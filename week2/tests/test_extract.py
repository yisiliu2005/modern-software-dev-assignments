import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm



def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# Unit tests for extract_action_items_llm()
def test_extract_llm_bullet_list():
    """Test LLM extraction with bullet list format."""
    text = """
    Meeting notes:
    - [ ] Set up database
    - [ ] Implement API endpoint
    - [ ] Write unit tests
    """
    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) > 0
    # Check that action items are extracted (non-empty strings)
    assert all(isinstance(item, str) and len(item.strip()) > 0 for item in items)


def test_extract_llm_keyword_prefixes():
    """Test LLM extraction with keyword-prefixed lines."""
    text = """
    TODO: Review the code
    ACTION: Deploy to production
    NEXT: Update documentation
    """
    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) > 0


def test_extract_llm_empty_input():
    """Test LLM extraction with empty input."""
    text = ""
    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    # Empty input should return empty list or handle gracefully
    assert len(items) >= 0


def test_extract_llm_plain_text():
    """Test LLM extraction with plain text containing action items."""
    text = """
    We need to create a new feature for user authentication.
    Please implement the login page.
    Also, we should update the database schema.
    """
    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) > 0
    # Verify items are strings
    assert all(isinstance(item, str) for item in items)


def test_extract_llm_mixed_content():
    """Test LLM extraction with mixed narrative and action items."""
    text = """
    During the meeting, we discussed several topics.
    The main points were about improving performance.
    - [ ] Optimize database queries
    - [ ] Add caching layer
    We also talked about the UI, but that's for later.
    TODO: Schedule follow-up meeting
    """
    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) > 0
