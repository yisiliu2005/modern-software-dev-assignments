# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Fix the extract_action_items_llm() function to use structured outputs (JSON) and return List[str]. The function should use Ollama's format="json" parameter for structured outputs, parse the JSON response, and handle errors gracefully with fallbacks.
``` 

Generated Code Snippets:
```
week2/app/services/extract.py:
- Lines 68-131: Complete implementation of extract_action_items_llm() function
  - Uses Ollama chat() with format="json" for structured outputs
  - Handles JSON parsing with markdown code block extraction
  - Includes error handling with fallbacks for network errors and parsing failures
  - Returns List[str] as required
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Write unit tests for extract_action_items_llm() covering multiple inputs: bullet lists, keyword-prefixed lines, empty input, plain text with action items, and mixed content scenarios. Each test should verify that the function returns a list of strings.
``` 

Generated Code Snippets:
```
week2/tests/test_extract.py:
- Lines 23-36: test_extract_llm_bullet_list() - Tests bullet list format extraction
- Lines 39-48: test_extract_llm_keyword_prefixes() - Tests keyword-prefixed lines (TODO:, ACTION:, NEXT:)
- Lines 51-57: test_extract_llm_empty_input() - Tests empty input handling
- Lines 60-71: test_extract_llm_plain_text() - Tests plain text with action items
- Lines 74-86: test_extract_llm_mixed_content() - Tests mixed narrative and action items
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Refactor the codebase for clarity: create Pydantic schemas for API contracts, improve error handling with proper HTTP status codes, enhance the database layer with better error handling and documentation, and improve app lifecycle management. Focus on well-defined API contracts, database layer cleanup, app lifecycle/configuration, and comprehensive error handling.
``` 

Generated/Modified Code Snippets:
```
week2/app/schemas.py:
- Entire file (lines 1-72): Created new file with Pydantic models
  - NoteBase, NoteCreate, NoteResponse (lines 13-30)
  - ActionItemBase, ActionItemResponse (lines 33-47)
  - ExtractRequest, ExtractResponse (lines 50-59)
  - MarkDoneRequest, MarkDoneResponse (lines 62-70)

week2/app/routers/notes.py:
- Lines 8: Added import for schemas
- Lines 14-45: Refactored create_note() to use NoteCreate/NoteResponse schemas with proper error handling
- Lines 48-70: Added list_notes() endpoint with proper error handling
- Lines 73-97: Refactored get_single_note() to use NoteResponse schema

week2/app/routers/action_items.py:
- Lines 9-15: Added imports for schemas
- Lines 21-63: Refactored extract() to use ExtractRequest/ExtractResponse schemas
- Lines 66-108: Added extract_llm() endpoint with proper error handling
- Lines 111-141: Refactored list_all() to use ActionItemResponse schema
- Lines 144-176: Refactored mark_done() to use MarkDoneRequest/MarkDoneResponse schemas

week2/app/db.py:
- Lines 1-5: Added module docstring
- Lines 22-40: Enhanced get_connection() and init_db() with error handling and documentation
- Lines 153-189: Enhanced insert_action_items() with better error handling (allows empty lists)
- Lines 191-216: Enhanced list_action_items() with documentation
- Lines 218-244: Added get_action_items_by_ids() function for efficient queries
- All database functions: Added comprehensive docstrings and error handling

week2/app/main.py:
- Lines 1-4: Added module docstring
- Lines 16-24: Enhanced FastAPI app initialization with metadata
- Lines 27-32: Added startup_event() for app lifecycle management
- Lines 35-38: Added shutdown_event() for cleanup
- Lines 41-50: Enhanced index() with error handling
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
1. Integrate the LLM-powered extraction as a new endpoint. Update the frontend to include an "Extract LLM" button that, when clicked, triggers the extraction process via the new endpoint.

2. Expose one final endpoint to retrieve all notes. Update the frontend to include a "List Notes" button that, when clicked, fetches and displays them.
``` 

Generated Code Snippets:
```
week2/app/routers/action_items.py:
- Lines 66-108: Added extract_llm() endpoint (POST /action-items/extract-llm)
  - Uses ExtractRequest/ExtractResponse schemas
  - Calls extract_action_items_llm() service function
  - Includes proper error handling

week2/app/routers/notes.py:
- Lines 48-70: Added list_notes() endpoint (GET /notes)
  - Returns all notes ordered by creation date
  - Uses NoteResponse schema
  - Includes proper error handling

week2/frontend/index.html:
- Line 27: Added "Extract LLM" button
- Line 28: Added "List Notes" button
- Line 32: Added notes display div
- Lines 39-58: Added renderActionItems() helper function
- Lines 83-104: Added event listener for "Extract LLM" button with timeout feedback
- Lines 106-133: Added event listener for "List Notes" button with notes display
- Lines 60-81: Enhanced "Extract" button with improved error handling
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Use Cursor to analyze the current codebase and generate a well-structured README.md file. The README should include: a brief overview of the project, how to set up and run the project, API endpoints and functionality, and instructions for running the test suite.
``` 

Generated Code Snippets:
```
week2/README.md:
- Entire file (lines 1-332): Created comprehensive README
  - Lines 1-12: Project overview and description
  - Lines 14-23: Features list
  - Lines 24-45: Project structure
  - Lines 47-91: Prerequisites, setup, and running instructions
  - Lines 93-231: Complete API endpoints documentation with examples
  - Lines 233-262: Test suite instructions and coverage
  - Lines 264-332: Additional sections (extraction methods, database schema, technology stack, development notes)
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 