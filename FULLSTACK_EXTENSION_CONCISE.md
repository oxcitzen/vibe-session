# Full-Stack Extension - Concise Prompt

## Task
Extend the existing CLI recipe recommendation system to a full-stack web application with FastAPI backend and minimal frontend (HTML/CSS/JavaScript), while preserving CLI functionality.

## Backend (FastAPI)

### New Files
- `app.py` - FastAPI application entry point
- `src/api.py` - API route definitions
- `src/schemas.py` - API request/response models

### API Endpoints
**POST `/api/recipes`**
- Request: `{"ingredients": "pasta, garlic, butter"}`
- Response: RecipeResponse JSON (existing model)
- Error handling with HTTP status codes

**GET `/`** - Serve frontend HTML
**GET `/health`** - Health check

### Requirements
- Reuse existing `RecipeGenerator` and models
- Enable CORS for frontend communication
- Serve static files from `static/` directory
- Extract `parse_ingredients` to shared utility if needed

## Frontend (Minimal)

### Files
- `templates/index.html` or `static/index.html`
- `static/style.css`
- `static/script.js`

### Features
- Input box for comma-separated ingredients
- Submit button
- Loading indicator
- Display area for recipe cards
- Error message display
- Responsive design

### JavaScript
- Use `fetch()` API for POST requests to `/api/recipes`
- Parse and display recipe JSON as formatted HTML
- Handle loading states and errors
- Client-side input validation

## File Structure
```
project_root/
├── app.py              # FastAPI server (NEW)
├── main.py             # CLI (KEEP EXISTING)
├── src/
│   ├── api.py          # FastAPI routes (NEW)
│   ├── schemas.py      # API models (NEW)
│   └── [existing files]
├── static/             # CSS, JS (NEW)
└── templates/          # HTML (NEW)
```

## Key Requirements
- ✅ Preserve CLI functionality in `main.py`
- ✅ Reuse existing recipe generation logic
- ✅ Minimal frontend (no frameworks)
- ✅ Secure CORS configuration
- ✅ Error handling on both ends
- ✅ Type hints and docstrings

## Running
- Web: `python app.py` or `uvicorn app:app --reload`
- CLI: `python main.py "ingredients"` (unchanged)
