from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..schemas import NoteCreate, NoteResponse


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> NoteResponse:
    """
    Create a new note.
    
    Args:
        note: Note creation request with content
        
    Returns:
        Created note with id and timestamp
        
    Raises:
        HTTPException: If note creation fails
    """
    try:
        note_id = db.insert_note(note.content)
        db_note = db.get_note(note_id)
        if db_note is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Note was created but could not be retrieved"
            )
        return NoteResponse(
            id=db_note["id"],
            content=db_note["content"],
            created_at=db_note["created_at"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create note: {str(e)}"
        )


@router.get("", response_model=List[NoteResponse])
def list_notes() -> List[NoteResponse]:
    """
    Retrieve all notes.
    
    Returns:
        List of all notes ordered by creation date (newest first)
    """
    try:
        notes = db.list_notes()
        return [
            NoteResponse(
                id=note["id"],
                content=note["content"],
                created_at=note["created_at"]
            )
            for note in notes
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve notes: {str(e)}"
        )


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """
    Retrieve a single note by ID.
    
    Args:
        note_id: The ID of the note to retrieve
        
    Returns:
        The requested note
        
    Raises:
        HTTPException: If note is not found
    """
    db_note = db.get_note(note_id)
    if db_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    return NoteResponse(
        id=db_note["id"],
        content=db_note["content"],
        created_at=db_note["created_at"]
    )


