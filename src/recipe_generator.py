"""Recipe generation using OpenAI API."""

import json
import logging
import time
from typing import List, Optional
from openai import OpenAI
from openai.types.chat import ChatCompletion

from src.config import Config
from src.models import RecipeResponse

logger = logging.getLogger(__name__)


class RecipeGenerator:
    """Handles recipe generation using OpenAI API."""
    
    def __init__(self):
        """Initialize the recipe generator with OpenAI client."""
        Config.validate()
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.temperature = Config.OPENAI_TEMPERATURE
        self.max_tokens = Config.OPENAI_MAX_TOKENS
        
        self.system_prompt = """You are a culinary expert assistant. Your task is to generate recipe recommendations based on provided ingredients.

CRITICAL: You MUST respond with ONLY valid JSON, no other text, no markdown, no explanations. Just pure JSON following this exact structure:
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
      },
      "dietaryRestrictions": ["vegan", "gluten-free"]
    }
  ]
}

Requirements:
- Generate 2-3 recipe suggestions
- Use the provided ingredients as the base
- Include realistic cooking times
- Provide accurate difficulty levels (must be exactly "Easy", "Medium", or "Hard")
- Estimate nutritional information realistically
- Instructions should be clear and actionable
- You may suggest additional common ingredients if needed for the recipe
- If the user provides dietary restrictions, ALL recipes MUST comply with them
- Always include the "dietaryRestrictions" array in each recipe (empty array if none)
- Return ONLY the JSON object, nothing else"""
    
    def generate_recipes(
        self,
        ingredients: List[str],
        dietary_restrictions: Optional[List[str]] = None,
        max_retries: int = 2,
    ) -> RecipeResponse:
        """
        Generate recipe recommendations based on ingredients.
        
        Args:
            ingredients: List of ingredient names
            dietary_restrictions: Optional list of dietary restrictions (e.g., vegan, gluten-free)
            max_retries: Maximum number of retry attempts for API calls
            
        Returns:
            RecipeResponse object with validated recipes
            
        Raises:
            ValueError: If API response is invalid or cannot be parsed
            Exception: If API call fails after retries
        """
        if not ingredients:
            raise ValueError("At least one ingredient is required")

        restrictions = [r.strip().lower() for r in (dietary_restrictions or []) if r.strip()]
        restrictions_str = ", ".join(restrictions)

        if restrictions:
            user_prompt = (
                "Generate 2-3 recipe suggestions using these ingredients: "
                f"{', '.join(ingredients)}. "
                "Dietary restrictions (MUST comply): "
                f"{restrictions_str}. "
                "If a restriction cannot be satisfied, adjust by suggesting substitutes and clearly reflect compliance."
            )
        else:
            user_prompt = f"Generate 2-3 recipe suggestions using these ingredients: {', '.join(ingredients)}"
        
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Generating recipes (attempt {attempt + 1}/{max_retries + 1})")
                
                response = self._call_openai_api(user_prompt)
                
                # Parse and validate response
                recipe_response = self._parse_response(response)

                # If restrictions were requested, ensure the model echoed them (at minimum)
                if restrictions:
                    for recipe in recipe_response.recipes:
                        # Normalize for comparison
                        got = {r.strip().lower() for r in (recipe.dietaryRestrictions or [])}
                        expected = set(restrictions)
                        # Not a hard fail (LLM may omit), but nudge stability by requiring echo
                        if not expected.issubset(got):
                            raise ValueError(
                                "Model output did not include all requested dietary restrictions "
                                f"in dietaryRestrictions. Expected at least: {restrictions_str}"
                            )
                
                logger.info(f"Successfully generated {len(recipe_response.recipes)} recipes")
                return recipe_response
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error on attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    raise ValueError(f"Failed to parse JSON response after {max_retries + 1} attempts: {e}")
                time.sleep(1)  # Brief delay before retry
                
            except Exception as e:
                logger.error(f"API call failed on attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    raise Exception(f"Failed to generate recipes after {max_retries + 1} attempts: {e}")
                time.sleep(1)  # Brief delay before retry
    
    def _supports_json_mode(self) -> bool:
        """
        Check if the current model supports JSON mode.
        
        JSON mode is supported by:
        - gpt-4-turbo, gpt-4-turbo-preview
        - gpt-4-1106-preview and newer gpt-4 models
        - gpt-3.5-turbo-1106 and newer gpt-3.5-turbo models
        - gpt-4o, gpt-4o-mini
        
        Returns:
            True if model supports JSON mode, False otherwise
        """
        # Models that support JSON mode (as of 2024)
        json_mode_models = [
            "gpt-4-turbo",
            "gpt-4-turbo-preview",
            "gpt-4-1106-preview",
            "gpt-4-0125-preview",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-0125",
            "gpt-4o",
            "gpt-4o-mini",
            "o1",
            "o1-preview",
        ]
        
        # Check if model name contains any of the supported models
        model_lower = self.model.lower()
        
        # Special case: newer gpt-3.5-turbo models (after 1106) support JSON mode
        if "gpt-3.5-turbo" in model_lower and any(
            ver in model_lower for ver in ["1106", "0125", "16k"]
        ):
            return True
        
        # Check against known supported models
        return any(supported in model_lower for supported in json_mode_models)
    
    def _call_openai_api(self, user_prompt: str, timeout: int = 30, use_json_mode: bool = True) -> ChatCompletion:
        """
        Make API call to OpenAI.
        
        Args:
            user_prompt: User's prompt with ingredients
            timeout: Request timeout in seconds
            use_json_mode: Whether to attempt using JSON mode
            
        Returns:
            ChatCompletion response from OpenAI
        """
        try:
            # Prepare base parameters
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "timeout": timeout
            }
            
            # Only add response_format if model supports it and use_json_mode is True
            if use_json_mode and self._supports_json_mode():
                params["response_format"] = {"type": "json_object"}
                logger.debug(f"Using JSON mode for model: {self.model}")
            elif use_json_mode:
                logger.warning(
                    f"Model {self.model} does not support JSON mode. "
                    "Relying on prompt engineering for JSON output."
                )
            
            response = self.client.chat.completions.create(**params)
            return response
            
        except Exception as e:
            error_str = str(e)
            # Check if it's the JSON mode error - retry without JSON mode
            if "response_format" in error_str and "json_object" in error_str and use_json_mode:
                logger.warning(
                    f"Model {self.model} does not support JSON mode. "
                    "Retrying without JSON mode (relying on prompt engineering)."
                )
                # Retry without JSON mode
                return self._call_openai_api(user_prompt, timeout, use_json_mode=False)
            
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _parse_response(self, response: ChatCompletion) -> RecipeResponse:
        """
        Parse and validate OpenAI response.
        
        Args:
            response: ChatCompletion response from OpenAI
            
        Returns:
            Validated RecipeResponse object
            
        Raises:
            ValueError: If response cannot be parsed or validated
        """
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("Empty response from OpenAI API")
        
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {content[:200]}")
            raise ValueError(f"Invalid JSON response: {e}")
        
        # Validate using Pydantic
        try:
            recipe_response = RecipeResponse(**data)
            return recipe_response
        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise ValueError(f"Response validation failed: {e}")
