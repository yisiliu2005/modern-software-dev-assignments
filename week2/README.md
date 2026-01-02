# Action Item Extractor

A FastAPI application that extracts actionable items from free-form notes using both heuristic-based and LLM-powered extraction methods. The application provides a web interface for inputting notes and automatically generating structured action item checklists.

## Overview

This application converts unstructured text notes into organized action items. It supports two extraction methods:

1. **Heuristic-based extraction**: Uses pattern matching to identify action items from bullet lists, checkboxes, and keyword-prefixed lines
2. **LLM-powered extraction**: Leverages Ollama and large language models to intelligently extract action items from natural language text

The application stores notes and action items in a SQLite database and provides a RESTful API for programmatic access.

## Features

- Extract action items from free-form text using rule-based heuristics
- Extract action items using LLM-powered natural language processing
- Save notes to the database for future reference
- List and retrieve all saved notes
- Mark action items as done/undone
- Filter action items by note ID
- Modern web interface for easy interaction

## Project Structure

```
week2/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── db.py                # Database layer with SQLite operations
│   ├── schemas.py           # Pydantic models for API contracts
│   ├── routers/
│   │   ├── notes.py         # Note management endpoints
│   │   └── action_items.py  # Action item extraction and management endpoints
│   └── services/
│       └── extract.py       # Extraction logic (heuristic and LLM)
├── frontend/
│   └── index.html          # Web interface
├── tests/
│   └── test_extract.py     # Unit tests for extraction functions
├── data/
│   └── app.db              # SQLite database (created automatically)
└── README.md               # This file
```

## Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Conda environment (cs146s) activated
- Ollama installed and running (for LLM-powered extraction)
- An Ollama model pulled (e.g., `mistral-nemo:12b-instruct-2407-q8_0`)

## Setup

1. **Activate your conda environment:**
   ```bash
   conda activate cs146s
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Set up Ollama (for LLM extraction):**
   - Install Ollama from https://ollama.com
   - Pull a model (recommended: start with a smaller model):
     ```bash
     ollama pull mistral-nemo:12b-instruct-2407-q8_0
     ```
   - Or use a different model from https://ollama.com/library

4. **Configure environment (optional):**
   - Create a `.env` file in the project root if you need custom configuration
   - The application uses `python-dotenv` to load environment variables

## Running the Application

1. **Start the development server:**
   ```bash
   poetry run uvicorn week2.app.main:app --reload
   ```

2. **Access the web interface:**
   - Open your browser and navigate to: http://127.0.0.1:8000/

3. **Access API documentation:**
   - Interactive API docs (Swagger UI): http://127.0.0.1:8000/docs
   - Alternative API docs (ReDoc): http://127.0.0.1:8000/redoc

## API Endpoints

### Notes Endpoints

#### `POST /notes`
Create a new note.

**Request Body:**
```json
{
  "content": "Your note content here"
}
```

**Response:**
```json
{
  "id": 1,
  "content": "Your note content here",
  "created_at": "2024-01-01 12:00:00"
}
```

#### `GET /notes`
Retrieve all notes, ordered by creation date (newest first).

**Response:**
```json
[
  {
    "id": 1,
    "content": "Note content",
    "created_at": "2024-01-01 12:00:00"
  }
]
```

#### `GET /notes/{note_id}`
Retrieve a specific note by ID.

**Response:**
```json
{
  "id": 1,
  "content": "Note content",
  "created_at": "2024-01-01 12:00:00"
}
```

### Action Items Endpoints

#### `POST /action-items/extract`
Extract action items from text using heuristic-based extraction.

**Request Body:**
```json
{
  "text": "Meeting notes:\n- [ ] Task 1\n- [ ] Task 2",
  "save_note": true
}
```

**Response:**
```json
{
  "note_id": 1,
  "items": [
    {
      "id": 1,
      "note_id": 1,
      "text": "Task 1",
      "done": false,
      "created_at": "2024-01-01 12:00:00"
    },
    {
      "id": 2,
      "note_id": 1,
      "text": "Task 2",
      "done": false,
      "created_at": "2024-01-01 12:00:00"
    }
  ]
}
```

#### `POST /action-items/extract-llm`
Extract action items from text using LLM-powered extraction.

**Request Body:**
```json
{
  "text": "We need to implement user authentication and update the database schema.",
  "save_note": true
}
```

**Response:** Same format as `/action-items/extract`

#### `GET /action-items`
List all action items, optionally filtered by note ID.

**Query Parameters:**
- `note_id` (optional): Filter action items by note ID

**Example:**
```
GET /action-items?note_id=1
```

**Response:**
```json
[
  {
    "id": 1,
    "note_id": 1,
    "text": "Task 1",
    "done": false,
    "created_at": "2024-01-01 12:00:00"
  }
]
```

#### `POST /action-items/{action_item_id}/done`
Mark an action item as done or not done.

**Request Body:**
```json
{
  "done": true
}
```

**Response:**
```json
{
  "id": 1,
  "done": true
}
```

## Running Tests

Run the test suite using pytest:

```bash
poetry run pytest week2/tests/
```

To run with verbose output:

```bash
poetry run pytest week2/tests/ -v
```

To run a specific test file:

```bash
poetry run pytest week2/tests/test_extract.py
```

### Test Coverage

The test suite includes:
- Tests for heuristic-based extraction (`extract_action_items`)
- Tests for LLM-powered extraction (`extract_action_items_llm`) covering:
  - Bullet list formats
  - Keyword-prefixed lines
  - Empty input handling
  - Plain text with action items
  - Mixed content scenarios

## Extraction Methods

### Heuristic-Based Extraction

The `extract_action_items()` function uses pattern matching to identify action items:
- Bullet points: `-`, `*`, `•`, or numbered lists
- Checkboxes: `[ ]` or `[todo]`
- Keyword prefixes: `todo:`, `action:`, `next:`
- Imperative sentences: Falls back to detecting imperative verbs (add, create, implement, fix, etc.)

### LLM-Powered Extraction

The `extract_action_items_llm()` function uses Ollama with structured JSON outputs:
- Sends text to the LLM with a system prompt for action item extraction
- Requests structured JSON output with an `action_items` array
- Handles markdown code blocks and JSON parsing errors gracefully
- Falls back to simple text parsing if JSON parsing fails

## Database Schema

The application uses SQLite with two main tables:

### `notes`
- `id`: INTEGER PRIMARY KEY
- `content`: TEXT NOT NULL
- `created_at`: TEXT DEFAULT (datetime('now'))

### `action_items`
- `id`: INTEGER PRIMARY KEY
- `note_id`: INTEGER (foreign key to notes.id)
- `text`: TEXT NOT NULL
- `done`: INTEGER DEFAULT 0 (0 = false, 1 = true)
- `created_at`: TEXT DEFAULT (datetime('now'))

## Technology Stack

- **FastAPI**: Modern Python web framework for building APIs
- **SQLite**: Lightweight database for local storage
- **Pydantic**: Data validation and settings management
- **Ollama**: Local LLM inference for action item extraction
- **Uvicorn**: ASGI server for running FastAPI

## Development

### Code Structure

The codebase follows a clean architecture pattern:
- **Routers**: Handle HTTP requests and responses
- **Schemas**: Define API contracts using Pydantic models
- **Services**: Contain business logic (extraction algorithms)
- **Database Layer**: Abstracts SQLite operations with proper error handling

### Error Handling

The application includes comprehensive error handling:
- HTTP status codes for different error scenarios
- Detailed error messages in API responses
- Database error handling with proper exception propagation
- Graceful fallbacks for LLM extraction failures

## License

This project is part of a course assignment.

## Contributing

This is a course assignment project. For questions or issues, please refer to the course materials.

