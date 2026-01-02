"""
FastAPI application for Action Item Extractor.
Main entry point for the application with proper lifecycle management.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .routers import action_items, notes

# Initialize database on application startup
init_db()

# Create FastAPI application with metadata
app = FastAPI(
    title="Action Item Extractor",
    description="A FastAPI application that extracts action items from free-form notes",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize application on startup."""
    # Database is already initialized at module level
    # This is a placeholder for any additional startup logic
    pass


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Clean up resources on shutdown."""
    # Placeholder for cleanup logic if needed
    pass


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """
    Serve the main HTML page.
    
    Returns:
        HTML content of the frontend page
    """
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "<html><body><h1>Frontend not found</h1></body></html>"


# Include routers
app.include_router(notes.router)
app.include_router(action_items.router)

# Mount static files
static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")