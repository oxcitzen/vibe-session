# Concise LLM Prompt for Recipe Backend Prototype

## Task
Create a minimal Python backend CLI application that recommends recipes based on ingredient input.

## Input Format
- CLI accepts comma-separated ingredients: `python main.py pasta, garlic, butter, parmesan`
- Parse and normalize ingredients (trim, lowercase)

## Output Format
Return structured JSON with exactly this schema:

```json
{
  "recipes": [
    {
      "name": "Recipe Name",
      "ingredients": ["ingredient1", "ingredient2"],
      "instructions": ["Step 1", "Step 2"],
      "cookingTime": "X minutes",
      "difficulty": "Easy|Medium|Hard",
      "nutrition": {
        "calories": integer,
        "protein": "Xg",
        "carbs": "Xg"
      }
    }
  ]
}
```

## Requirements
1. Generate 2-3 recipe suggestions per request
2. Use OpenAI API (API key from `.env` file)
3. Force JSON output using OpenAI's JSON mode
4. Validate output with Pydantic models
5. Display formatted JSON in CLI

## File Structure
```
project_root/
├── .env                    # OPENAI_API_KEY
├── .gitignore
├── requirements.txt
├── main.py                 # CLI entry point
└── src/
    ├── __init__.py
    ├── recipe_generator.py # OpenAI integration
    ├── models.py           # Pydantic schemas
    └── config.py           # Config/env loading
```

## OpenAI System Prompt
```
You are a culinary expert. Generate 2-3 recipe suggestions using the provided ingredients.

Respond ONLY with valid JSON matching this structure:
{
  "recipes": [
    {
      "name": "string",
      "ingredients": ["string"],
      "instructions": ["string"],
      "cookingTime": "string",
      "difficulty": "Easy|Medium|Hard",
      "nutrition": {
        "calories": integer,
        "protein": "string",
        "carbs": "string"
      }
    }
  ]
}
```

## Error Handling
- Missing API key
- API failures (retry 2x)
- Invalid JSON responses
- Network errors
- Empty/invalid input

## Code Quality
- Type hints
- Docstrings
- PEP 8 compliance
- Pydantic validation
- Logging

## Dependencies
- openai
- python-dotenv
- pydantic
