from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique

def extract_action_items_llm(text: str) -> List[str]:
    """
    Extract action items from text using an LLM (Ollama).
    Uses structured outputs to return a JSON array of action item strings.
    """
    # Handle empty input
    if not text or not text.strip():
        return []
    
    system_prompt = """You are a helpful assistant that extracts action items from text.
Extract all actionable items from the given text and return them as a JSON object with an "action_items" array.
Each action item should be a clear, concise string describing what needs to be done.
Return ONLY valid JSON, no other text."""
    
    user_prompt = f"""Extract action items from the following text:
{text}

Return the result as JSON with this structure:
{{"action_items": ["item1", "item2", ...]}}"""
    
    response = None
    try:
        response = chat(
            model="mistral-nemo:12b-instruct-2407-q8_0",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            format="json"
        )
        
        # Parse the JSON response
        content = response.message.content.strip()
        # Handle cases where the response might be wrapped in markdown code blocks
        if content.startswith("```"):
            # Extract JSON from code block
            lines = content.split("\n")
            json_lines = [line for line in lines if not line.strip().startswith("```")]
            content = "\n".join(json_lines)
        
        parsed = json.loads(content)
        action_items = parsed.get("action_items", [])
        
        # Ensure we return a list of strings
        if isinstance(action_items, list):
            return [str(item).strip() for item in action_items if item]
        return []
    except (json.JSONDecodeError, KeyError, AttributeError):
        # Fallback: try to extract from plain text response
        # This handles cases where the model doesn't return valid JSON
        if response and hasattr(response, 'message') and hasattr(response.message, 'content'):
            try:
                content = response.message.content
                # Simple fallback: split by newlines and clean
                items = [line.strip() for line in content.split("\n") if line.strip() and not line.strip().startswith("#")]
                return items[:10]  # Limit to 10 items as fallback
            except Exception:
                pass
        # If all else fails, return empty list
        return []
    except Exception as e:
        # Handle network errors, model not found, etc.
        # Log the error for debugging but return empty list to gracefully handle failures
        import logging
        logging.warning(f"LLM extraction failed: {str(e)}")
        return []

def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
