# Full-Stack Extension Prompt - Recipe Recommendation System

## Overview
Extend the existing CLI-based recipe recommendation backend to a full-stack web application with a minimal frontend (HTML, CSS, JavaScript) and FastAPI backend, while maintaining the existing CLI functionality.

## Current Architecture
The existing codebase has:
- CLI entry point (`main.py`)
- Core recipe generation logic (`src/recipe_generator.py`)
- Pydantic models (`src/models.py`)
- Configuration management (`src/config.py`)
- All dependencies already in `requirements.txt` (including FastAPI)

## Extension Requirements

### 1. Backend API (FastAPI)

#### 1.1 API Endpoints
Create a FastAPI application with the following endpoints:

**POST `/api/recipes`**
- **Purpose**: Generate recipe recommendations from ingredients
- **Request Body**:
  ```json
  {
    "ingredients": "pasta, garlic, butter, parmesan"
  }
  ```
- **Response**: 
  ```json
  {
    "recipes": [
      {
        "name": "Garlic Butter Pasta",
        "ingredients": ["pasta", "garlic", "butter", "parmesan"],
        "instructions": ["Step 1", "Step 2"],
        "cookingTime": "20 minutes",
        "difficulty": "Easy",
        "nutrition": {
          "calories": 450,
          "protein": "12g",
          "carbs": "60g"
        }
      }
    ]
  }
  ```
- **Error Handling**: Return appropriate HTTP status codes (400 for validation errors, 500 for server errors)
- **Validation**: Use Pydantic request/response models

**GET `/`**
- **Purpose**: Serve the main HTML page
- **Response**: HTML file with the frontend interface

**GET `/health`**
- **Purpose**: Health check endpoint
- **Response**: `{"status": "healthy"}`

#### 1.2 File Structure
Create new files:
- `src/api.py` - FastAPI application setup and route definitions
- `src/schemas.py` - Pydantic request/response schemas for API
- `app.py` - Main FastAPI application entry point (separate from CLI)

#### 1.3 CORS Configuration
- Enable CORS for frontend-backend communication
- Configure appropriate origins (allow localhost for development)

#### 1.4 Static Files
- Serve static files (CSS, JavaScript) from a `static/` directory
- Serve HTML templates from a `templates/` directory (if using Jinja2) or serve directly

### 2. Frontend (Minimal HTML/CSS/JavaScript)

#### 2.1 HTML Structure
Create `templates/index.html` or `static/index.html` with:
- **Input Section**:
  - Text input or textarea for comma-separated ingredients
  - Submit button
  - Clear/reset button
  - Input validation feedback
- **Output Section**:
  - Container to display recipe recommendations
  - Loading indicator/spinner
  - Error message display area
- **Recipe Display**:
  - Display each recipe in a card/container
  - Show all recipe fields (name, ingredients, instructions, cooking time, difficulty, nutrition)
  - Format instructions as a numbered or bulleted list
  - Make it visually appealing and readable

#### 2.2 CSS Styling
Create `static/style.css` with:
- Modern, clean design
- Responsive layout (works on desktop and mobile)
- Proper spacing and typography
- Color scheme that's easy to read
- Loading spinner animation
- Recipe card styling
- Error message styling
- Button hover effects

#### 2.3 JavaScript Functionality
Create `static/script.js` with:
- **API Communication**:
  - Function to send POST request to `/api/recipes`
  - Handle response and errors
  - Display loading state during API call
- **Input Handling**:
  - Parse comma-separated ingredients
  - Validate input (at least one ingredient)
  - Clear previous results on new submission
- **Display Logic**:
  - Render recipes dynamically in the DOM
  - Format JSON response into readable HTML
  - Handle and display error messages
  - Show/hide loading indicators

### 3. File Structure

```
project_root/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── main.py                    # CLI entry point (keep existing)
├── app.py                     # FastAPI web server entry point (NEW)
├── src/
│   ├── __init__.py
│   ├── config.py              # Existing
│   ├── models.py              # Existing
│   ├── recipe_generator.py    # Existing
│   ├── api.py                 # FastAPI routes (NEW)
│   └── schemas.py             # API request/response models (NEW)
├── static/                    # Static files (NEW)
│   ├── style.css
│   └── script.js
└── templates/                 # HTML templates (NEW)
    └── index.html
```

### 4. Implementation Details

#### 4.1 Backend API Implementation
- **Reuse Existing Logic**: 
  - Import and use `RecipeGenerator` from `src/recipe_generator.py`
  - Import and use `parse_ingredients` function (extract from `main.py` or create utility)
  - Use existing Pydantic models from `src/models.py`
  
- **API Request Schema**:
  ```python
  class RecipeRequest(BaseModel):
      ingredients: str = Field(..., min_length=1, description="Comma-separated ingredients")
  ```

- **API Response Schema**:
  - Reuse `RecipeResponse` from `src/models.py` or create API-specific response model

- **Error Handling**:
  - Use FastAPI's HTTPException for proper error responses
  - Return structured error messages: `{"error": "error message"}`
  - Handle validation errors, API errors, and network errors

#### 4.2 Frontend Implementation
- **API Endpoint**: Use relative URLs (e.g., `/api/recipes`) or configure base URL
- **Fetch API**: Use native `fetch()` for HTTP requests (no external libraries)
- **Error Handling**: Display user-friendly error messages
- **Loading States**: Show spinner/loading indicator during API calls
- **Input Validation**: Client-side validation before submitting

#### 4.3 Security Considerations
- **Input Sanitization**: Sanitize user input to prevent XSS
- **CORS**: Configure CORS appropriately (allow only necessary origins)
- **Rate Limiting**: Consider basic rate limiting (optional for prototype)
- **Input Validation**: Validate all inputs on both client and server side

### 5. Running the Application

#### 5.1 Web Server
- Create `app.py` that runs FastAPI with uvicorn
- Default port: 8000
- Command: `python app.py` or `uvicorn app:app --reload`

#### 5.2 CLI (Preserve Existing)
- Keep `main.py` functional for CLI usage
- CLI and web server should work independently

### 6. Code Quality Requirements

- **Type Hints**: Use type hints throughout
- **Docstrings**: Add docstrings to all functions and classes
- **Error Handling**: Comprehensive error handling on both frontend and backend
- **Logging**: Use Python logging for API requests and errors
- **Code Reuse**: Maximize reuse of existing code (don't duplicate logic)

### 7. User Experience

- **Loading Feedback**: Show clear loading indicators
- **Error Messages**: Display clear, actionable error messages
- **Success Feedback**: Visually indicate successful recipe generation
- **Responsive Design**: Works well on different screen sizes
- **Accessibility**: Use semantic HTML, proper labels, ARIA attributes where needed

### 8. Testing the Extension

After implementation, verify:
- [ ] Frontend loads correctly at root URL
- [ ] Can submit ingredients and receive recipes
- [ ] Recipes display in readable format
- [ ] Error messages display correctly
- [ ] Loading indicators work
- [ ] CLI still works independently
- [ ] CORS is configured correctly
- [ ] Static files are served correctly

## Additional Recommendations

### 9. Enhancements (Optional for Prototype)
- Add input suggestions/autocomplete for common ingredients
- Add ability to copy recipe to clipboard
- Add print-friendly recipe view
- Add recipe card animations
- Add ingredient tags/chips display
- Add dark mode toggle

### 10. Documentation
- Update README.md with:
  - How to run the web server
  - How to access the frontend
  - API endpoint documentation
  - Environment variable setup

## Implementation Notes

- **Preserve CLI**: The existing CLI functionality in `main.py` must remain intact
- **Code Reuse**: Extract common functions (like `parse_ingredients`) to a shared utility module if needed
- **Separation of Concerns**: Keep API logic separate from CLI logic
- **Minimal Frontend**: Keep frontend simple - no frameworks, just vanilla HTML/CSS/JavaScript
- **FastAPI Best Practices**: Follow FastAPI conventions for route definitions and dependency injection

## Example API Usage

```javascript
// Frontend JavaScript example
async function getRecipes(ingredients) {
    const response = await fetch('/api/recipes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ingredients: ingredients })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to fetch recipes');
    }
    
    return await response.json();
}
```

## Validation Checklist

Before considering complete:
- [ ] FastAPI server starts without errors
- [ ] Frontend page loads and displays correctly
- [ ] Can submit ingredients via web interface
- [ ] Recipes are displayed in readable format
- [ ] Error handling works on both frontend and backend
- [ ] CLI functionality still works
- [ ] CORS is properly configured
- [ ] Static files are served correctly
- [ ] API returns correct JSON structure
- [ ] Input validation works on both client and server
