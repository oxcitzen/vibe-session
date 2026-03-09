"""FastAPI routes for the recipe recommendation system."""

import logging

from fastapi import APIRouter, HTTPException

from src.recipe_generator import RecipeGenerator
from src.schemas import RecipeRequest, RecipeResponseSchema
from src.utils import parse_ingredients, parse_user_input

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@router.post("/api/recipes", response_model=RecipeResponseSchema)
def generate_recipes(payload: RecipeRequest) -> RecipeResponseSchema:
    """
    Generate 2-3 recipe suggestions from comma-separated ingredients.
    """
    try:
        # Accept either:
        # - payload.ingredients = "a, b, c | vegan, gluten-free"
        # - payload.ingredients = "a, b, c" AND payload.dietaryRestrictions = "vegan, gluten-free"
        ingredients, restrictions_from_input = parse_user_input(payload.ingredients)
        restrictions_from_field = []
        if payload.dietaryRestrictions:
            restrictions_from_field = [
                r.strip().lower()
                for r in payload.dietaryRestrictions.split(",")
                if r.strip()
            ]
        dietary_restrictions = restrictions_from_field or restrictions_from_input
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    try:
        generator = RecipeGenerator()
        return generator.generate_recipes(ingredients, dietary_restrictions=dietary_restrictions)
    except ValueError as e:
        # Covers invalid/malformed model output or validation errors
        logger.error("Recipe generation validation error: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        logger.exception("Recipe generation failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to generate recipes") from e

