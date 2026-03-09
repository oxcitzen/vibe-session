# Recipe Recommendation (CLI + Web)

A minimal prototype that generates recipe recommendations based on ingredient input using OpenAI's LLM.

You can use it as:
- **CLI app** (`main.py`)
- **Full-stack web app** (FastAPI backend + minimal HTML/CSS/JS frontend via `app.py`)

## Features

- Accepts comma-separated ingredients via CLI
- Minimal web UI with an ingredient input box
- Optional dietary restrictions filtering (e.g., vegan, gluten-free)
- Generates 2-3 recipe suggestions using OpenAI API
- Returns structured JSON output with:
  - Recipe name and ingredients
  - Step-by-step instructions
  - Cooking time and difficulty level
  - Basic nutritional information
  - Dietary restrictions each recipe complies with
- Validates output using Pydantic models
- Robust error handling and retry logic

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4-turbo
   OPENAI_TEMPERATURE=0.7
   OPENAI_MAX_TOKENS=2000
   ```
   
   **Note on Models**: For best results with structured JSON output, use models that support JSON mode:
   - `gpt-4-turbo` (recommended)
   - `gpt-4o` or `gpt-4o-mini`
   - `gpt-3.5-turbo` (newer versions)
   
   The application will automatically fall back to prompt-based JSON generation if your model doesn't support JSON mode.

## Usage (Web App)

Start the FastAPI server:

```bash
python app.py
```

Then open:
- `http://127.0.0.1:8000/`

In the web UI you can enter:
- **Ingredients**: `pasta, garlic, butter, parmesan`
- **Dietary restrictions (optional)**: `vegan, gluten-free`

### API

- **POST** `/api/recipes`
  - **Body**:
    ```json
    { "ingredients": "pasta, garlic, butter, parmesan" }
    ```
  - **Response**: structured JSON `RecipeResponse`
  - **Dietary restrictions** (either option):
    - **Option A (preferred)**: add a separate field:
      ```json
      { "ingredients": "pasta, garlic, butter, parmesan", "dietaryRestrictions": "vegan, gluten-free" }
      ```
    - **Option B**: append to the ingredients string:
      ```json
      { "ingredients": "pasta, garlic, butter, parmesan | vegan, gluten-free" }
      ```

- **GET** `/health`
  - Returns: `{"status":"healthy"}`

## Usage (CLI)

Run the CLI with comma-separated ingredients:

```bash
python main.py pasta, garlic, butter, parmesan
```

Or with quotes for better parsing:

```bash
python main.py "pasta, garlic, butter, parmesan"
```

### CLI with dietary restrictions

Append restrictions at the end using `|` (or `;`):

```bash
python main.py "pasta, garlic, butter, parmesan | vegan, gluten-free"
```

## Example Output

```json
{
  "recipes": [
    {
      "name": "Garlic Butter Pasta",
      "ingredients": ["pasta", "garlic", "butter", "parmesan"],
      "instructions": [
        "Boil pasta according to package instructions",
        "Sauté garlic in butter until fragrant",
        "Toss pasta with garlic butter and parmesan"
      ],
      "cookingTime": "20 minutes",
      "difficulty": "Easy",
      "nutrition": {
        "calories": 450,
        "protein": "12g",
        "carbs": "60g"
      },
      "dietaryRestrictions": []
    }
  ]
}
```

## Project Structure

```
project_root/
├── .env                    # Environment variables (not in git)
├── .gitignore
├── requirements.txt
├── README.md
├── main.py                 # CLI entry point
├── app.py                  # FastAPI web server entry point
├── static/                 # Frontend assets (CSS/JS)
│   ├── style.css
│   └── script.js
├── templates/              # Frontend HTML
│   └── index.html
└── src/
    ├── __init__.py
    ├── recipe_generator.py  # OpenAI integration
    ├── models.py            # Pydantic schemas
    ├── config.py            # Config/env loading
    ├── utils.py             # Shared parsing utilities
    ├── api.py               # FastAPI routes
    └── schemas.py           # API request schemas
```

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in `requirements.txt`

## Error Handling

The application handles:
- Missing API key
- API failures (with retry logic)
- Invalid JSON responses
- Network errors
- Empty/invalid input

## License

MIT
