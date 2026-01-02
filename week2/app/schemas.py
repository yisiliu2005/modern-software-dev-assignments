"""
Pydantic schemas for API request/response models.
Defines well-structured API contracts for type safety and validation.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base schema for note data."""
    content: str = Field(..., min_length=1, description="The note content")


class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


class NoteResponse(BaseModel):
    """Schema for note response."""
    id: int
    content: str
    created_at: str

    class Config:
        from_attributes = True


class ActionItemBase(BaseModel):
    """Base schema for action item data."""
    text: str = Field(..., min_length=1, description="The action item text")


class ActionItemResponse(BaseModel):
    """Schema for action item response."""
    id: int
    note_id: Optional[int] = None
    text: str
    done: bool
    created_at: str

    class Config:
        from_attributes = True


class ExtractRequest(BaseModel):
    """Schema for action item extraction request."""
    text: str = Field(..., min_length=1, description="Text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the text as a note")


class ExtractResponse(BaseModel):
    """Schema for action item extraction response."""
    note_id: Optional[int] = None
    items: List[ActionItemResponse]


class MarkDoneRequest(BaseModel):
    """Schema for marking an action item as done."""
    done: bool = Field(default=True, description="Whether the action item is done")


class MarkDoneResponse(BaseModel):
    """Schema for marking action item done response."""
    id: int
    done: bool

