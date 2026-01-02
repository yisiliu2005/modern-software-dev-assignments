"""
Database layer for SQLite operations.
Provides a clean interface for database operations with proper error handling.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

# Database configuration
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


def ensure_data_directory_exists() -> None:
    """Ensure the data directory exists for the database file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """
    Get a database connection with row factory configured.
    
    Returns:
        SQLite connection with Row factory for dict-like access
        
    Raises:
        sqlite3.Error: If connection fails
    """
    ensure_data_directory_exists()
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to connect to database: {str(e)}") from e


def init_db() -> None:
    """
    Initialize the database schema.
    Creates tables if they don't exist.
    
    Raises:
        sqlite3.Error: If schema initialization fails
    """
    ensure_data_directory_exists()
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now'))
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS action_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER,
                    text TEXT NOT NULL,
                    done INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (note_id) REFERENCES notes(id)
                );
                """
            )
            connection.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to initialize database schema: {str(e)}") from e


def insert_note(content: str) -> int:
    """
    Insert a new note into the database.
    
    Args:
        content: The note content
        
    Returns:
        The ID of the newly created note
        
    Raises:
        sqlite3.Error: If insertion fails
        ValueError: If content is empty
    """
    if not content or not content.strip():
        raise ValueError("Note content cannot be empty")
    
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            connection.commit()
            note_id = int(cursor.lastrowid)
            if note_id == 0:
                raise RuntimeError("Failed to insert note: no ID returned")
            return note_id
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to insert note: {str(e)}") from e


def list_notes() -> list[sqlite3.Row]:
    """
    List all notes ordered by ID (newest first).
    
    Returns:
        List of note rows with id, content, and created_at
        
    Raises:
        sqlite3.Error: If query fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
            return list(cursor.fetchall())
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to list notes: {str(e)}") from e


def get_note(note_id: int) -> Optional[sqlite3.Row]:
    """
    Get a single note by ID.
    
    Args:
        note_id: The ID of the note to retrieve
        
    Returns:
        Note row if found, None otherwise
        
    Raises:
        sqlite3.Error: If query fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            return cursor.fetchone()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to get note: {str(e)}") from e


def insert_action_items(items: list[str], note_id: Optional[int] = None) -> list[int]:
    """
    Insert multiple action items into the database.
    
    Args:
        items: List of action item text strings
        note_id: Optional note ID to associate with action items
        
    Returns:
        List of IDs for the newly created action items (empty list if no items provided)
        
    Raises:
        sqlite3.Error: If insertion fails
    """
    # Allow empty lists - just return empty list of IDs
    if not items:
        return []
    
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            ids: list[int] = []
            for item in items:
                if not item or not item.strip():
                    continue  # Skip empty items
                cursor.execute(
                    "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                    (note_id, item.strip()),
                )
                ids.append(int(cursor.lastrowid))
            connection.commit()
            return ids
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to insert action items: {str(e)}") from e


def list_action_items(note_id: Optional[int] = None) -> list[sqlite3.Row]:
    """
    List action items, optionally filtered by note_id.
    
    Args:
        note_id: Optional note ID to filter action items
        
    Returns:
        List of action item rows with id, note_id, text, done, and created_at
        
    Raises:
        sqlite3.Error: If query fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            if note_id is None:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
                )
            else:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                    (note_id,),
                )
            return list(cursor.fetchall())
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to list action items: {str(e)}") from e


def get_action_items_by_ids(item_ids: list[int]) -> list[sqlite3.Row]:
    """
    Get action items by their IDs.
    
    Args:
        item_ids: List of action item IDs to retrieve
        
    Returns:
        List of action item rows with id, note_id, text, done, and created_at
        
    Raises:
        sqlite3.Error: If query fails
    """
    if not item_ids:
        return []
    
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            # Use IN clause with parameterized query
            placeholders = ",".join("?" * len(item_ids))
            cursor.execute(
                f"SELECT id, note_id, text, done, created_at FROM action_items WHERE id IN ({placeholders})",
                item_ids,
            )
            return list(cursor.fetchall())
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to get action items by IDs: {str(e)}") from e


def mark_action_item_done(action_item_id: int, done: bool) -> None:
    """
    Mark an action item as done or not done.
    
    Args:
        action_item_id: The ID of the action item to update
        done: Whether the action item is done
        
    Raises:
        sqlite3.Error: If update fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Action item with id {action_item_id} not found")
            connection.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to update action item: {str(e)}") from e


