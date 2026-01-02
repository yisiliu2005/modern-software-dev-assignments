from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

from .. import db
from ..services.extract import extract_action_items, extract_action_items_llm
from ..schemas import (
    ExtractRequest,
    ExtractResponse,
    ActionItemResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(request: ExtractRequest) -> ExtractResponse:
    """
    Extract action items from text using heuristic-based extraction.
    
    Args:
        request: Extraction request with text and optional save_note flag
        
    Returns:
        Extracted action items with optional note_id if saved
        
    Raises:
        HTTPException: If extraction fails
    """
    try:
        note_id: Optional[int] = None
        if request.save_note:
            note_id = db.insert_note(request.text)

        items = extract_action_items(request.text)
        ids = db.insert_action_items(items, note_id=note_id)
        
        # If no items were extracted, return empty list
        if not ids:
            return ExtractResponse(note_id=note_id, items=[])
        
        # Fetch only the items we just inserted to get created_at timestamps
        db_items = db.get_action_items_by_ids(ids)
        items_by_id = {item["id"]: item for item in db_items}
        
        action_items = [
            ActionItemResponse(
                id=item_id,
                note_id=note_id,
                text=item_text,
                done=False,
                created_at=items_by_id[item_id]["created_at"] if item_id in items_by_id else ""
            )
            for item_id, item_text in zip(ids, items)
        ]
        
        return ExtractResponse(note_id=note_id, items=action_items)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract action items: {str(e)}"
        )


@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(request: ExtractRequest) -> ExtractResponse:
    """
    Extract action items from text using LLM-powered extraction.
    
    Args:
        request: Extraction request with text and optional save_note flag
        
    Returns:
        Extracted action items with optional note_id if saved
        
    Raises:
        HTTPException: If extraction fails
    """
    try:
        note_id: Optional[int] = None
        if request.save_note:
            note_id = db.insert_note(request.text)

        items = extract_action_items_llm(request.text)
        ids = db.insert_action_items(items, note_id=note_id)
        
        # If no items were extracted, return empty list
        if not ids:
            return ExtractResponse(note_id=note_id, items=[])
        
        # Fetch only the items we just inserted to get created_at timestamps
        db_items = db.get_action_items_by_ids(ids)
        items_by_id = {item["id"]: item for item in db_items}
        
        action_items = [
            ActionItemResponse(
                id=item_id,
                note_id=note_id,
                text=item_text,
                done=False,
                created_at=items_by_id[item_id]["created_at"] if item_id in items_by_id else ""
            )
            for item_id, item_text in zip(ids, items)
        ]
        
        return ExtractResponse(note_id=note_id, items=action_items)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract action items with LLM: {str(e)}"
        )


@router.get("", response_model=List[ActionItemResponse])
def list_all(note_id: Optional[int] = Query(None, description="Filter by note ID")) -> List[ActionItemResponse]:
    """
    List all action items, optionally filtered by note_id.
    
    Args:
        note_id: Optional note ID to filter action items
        
    Returns:
        List of action items
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        rows = db.list_action_items(note_id=note_id)
        return [
            ActionItemResponse(
                id=r["id"],
                note_id=r["note_id"],
                text=r["text"],
                done=bool(r["done"]),
                created_at=r["created_at"],
            )
            for r in rows
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve action items: {str(e)}"
        )


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, request: MarkDoneRequest) -> MarkDoneResponse:
    """
    Mark an action item as done or not done.
    
    Args:
        action_item_id: The ID of the action item to update
        request: Request with done status
        
    Returns:
        Updated action item with done status
        
    Raises:
        HTTPException: If update fails or action item not found
    """
    try:
        # Verify action item exists
        all_items = db.list_action_items()
        if not any(item["id"] == action_item_id for item in all_items):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Action item with id {action_item_id} not found"
            )
        
        db.mark_action_item_done(action_item_id, request.done)
        return MarkDoneResponse(id=action_item_id, done=request.done)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update action item: {str(e)}"
        )


