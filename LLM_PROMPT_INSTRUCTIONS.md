# Backend Recipe Recommendation Prototype - LLM Instructions

## Project Overview
Create a minimal backend prototype that takes a comma-separated list of ingredients as input via CLI and uses an LLM to generate recipe recommendations with structured JSON output.

## Core Requirements

### 1. Input/Output Format
- **Input**: Comma-separated list of ingredients via CLI (e.g., `"pasta", "garlic", "butter", "parmesan"`)
- **Output**: Display structured JSON response in CLI
- **Processing**: Use OpenAI API to generate recipe recommendations

### 2. JSON Output Structure
The LLM must return responses in the following exact JSON format:

```json
{
  "recipes": [
    {
      "name": "Garlic Butter Pasta",
      "ingredients": ["pasta", "garlic", "butter", "parmesan"],
      "instructions": ["Boil pasta...", "Sauté garlic..."],
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

### 3. Recipe Generation Requirements
- Generate **2-3 recipe suggestions** using the provided ingredients
- Each recipe must include:
  - Recipe name
  - List of ingredients (including the provided ones)
  - Step-by-step instructions (as array of strings)
  - Estimated cooking time (as string, e.g., "20 minutes")
  - Difficulty level (one of: "Easy", "Medium", "Hard")
  - Basic nutritional information:
    - calories (as integer)
    - protein (as string with unit, e.g., "12g")
    - carbs (as string with unit, e.g., "60g")

### 4. File Structure
Create the following file structure:

```
project_root/
├── .env                    # Environment variables (OpenAI API key)
├── .gitignore              # Git ignore file (include .env)
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── main.py                # Main CLI entry point
├── src/
│   ├── __init__.py
│   ├── recipe_generator.py    # Core recipe generation logic
│   ├── models.py              # Pydantic models for data validation
│   └── config.py              # Configuration management
└── tests/
    └── __init__.py
```

## Implementation Details

### 5. Environment Variables
- Use `.env` file to store `OPENAI_API_KEY`
- Load environment variables using `python-dotenv`
- Include `.env` in `.gitignore`
- Provide `.env.example` template file

### 6. OpenAI API Integration
- Use OpenAI API with structured output (JSON mode)
- Implement proper error handling for API failures
- Include retry logic for transient failures (max 2 retries)
- Set appropriate temperature (0.7) for creative but consistent output
- Use a system prompt that enforces JSON structure

### 7. Input Processing
- Parse comma-separated ingredients from CLI
- Clean and normalize ingredient names (trim whitespace, lowercase)
- Validate that at least one ingredient is provided
- Handle edge cases (empty input, special characters)

### 8. Output Validation
- Use Pydantic models to validate JSON structure before returning
- Ensure all required fields are present
- Validate data types (integers for calories, strings for others)
- Handle malformed JSON responses gracefully

### 9. CLI Interface
- Create a simple, user-friendly CLI interface
- Display input ingredients clearly
- Pretty-print JSON output with proper indentation
- Show error messages in a clear format
- Include a help message/usage instructions

### 10. Error Handling
- Handle missing API key gracefully
- Handle API rate limits and errors
- Handle invalid JSON responses from LLM
- Handle network errors
- Provide meaningful error messages to users

## System Prompt for OpenAI API

Use the following system prompt to ensure structured output:

```
You are a culinary expert assistant. Your task is to generate recipe recommendations based on provided ingredients.

IMPORTANT: You MUST respond with valid JSON only, following this exact structure:
{
  "recipes": [
    {
      "name": "Recipe Name",
      "ingredients": ["ingredient1", "ingredient2"],
      "instructions": ["Step 1", "Step 2"],
      "cookingTime": "X minutes",
      "difficulty": "Easy|Medium|Hard",
      "nutrition": {
        "calories": number,
        "protein": "Xg",
        "carbs": "Xg"
      }
    }
  ]
}

Requirements:
- Generate 2-3 recipe suggestions
- Use the provided ingredients as the base
- Include realistic cooking times
- Provide accurate difficulty levels
- Estimate nutritional information realistically
- Instructions should be clear and actionable
```

## Code Quality Requirements

### 11. Best Practices
- Use type hints throughout the codebase
- Add docstrings to all functions and classes
- Follow PEP 8 style guidelines
- Use Pydantic for data validation
- Implement logging for debugging (use Python's logging module)
- Add basic input sanitization

### 12. Dependencies
Ensure `requirements.txt` includes:
- `openai` (latest stable version)
- `python-dotenv` (for environment variables)
- `pydantic` (for data validation)
- `typing` (for type hints - built-in)

### 13. Testing Considerations
- Structure code to be testable
- Separate business logic from API calls
- Use dependency injection for OpenAI client

## Example Usage Flow

1. User runs: `python main.py pasta, garlic, butter, parmesan`
2. System parses ingredients: `["pasta", "garlic", "butter", "parmesan"]`
3. System calls OpenAI API with system prompt and user ingredients
4. System validates JSON response against Pydantic model
5. System displays formatted JSON in CLI

## Additional Stability Recommendations

### 14. Robustness Features
- Add timeout for API calls (30 seconds)
- Implement request/response logging
- Add validation for ingredient count (minimum 1, maximum 20)
- Sanitize ingredient names (remove special characters that might break JSON)
- Use JSON schema validation in addition to Pydantic
- Implement response caching (optional, for development)

### 15. Configuration
- Make OpenAI model configurable (default: "gpt-4" or "gpt-3.5-turbo")
- Allow temperature adjustment via environment variable
- Add max_tokens limit (suggest 2000)

### 16. User Experience
- Show loading indicator while processing
- Display processing time
- Format JSON output with colors (optional, using libraries like `rich` or `colorama`)
- Add option to save output to file

## Validation Checklist

Before considering the prototype complete, ensure:
- [ ] All required fields are present in JSON output
- [ ] JSON structure matches exactly the specified format
- [ ] Error handling works for all edge cases
- [ ] Environment variables are loaded correctly
- [ ] CLI accepts comma-separated ingredients
- [ ] Output is properly formatted and readable
- [ ] Code follows Python best practices
- [ ] All dependencies are listed in requirements.txt
- [ ] .env file is in .gitignore

## Notes for Implementation
- Keep the codebase minimal but functional
- Prioritize correctness over features
- Ensure the JSON output is always valid and parseable
- Test with various ingredient combinations
- Handle cases where LLM might suggest recipes with additional ingredients beyond the input list
