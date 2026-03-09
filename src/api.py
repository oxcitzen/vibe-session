"""FastAPI routes for the recipe recommendation system."""

import logging

from fastapi import APIRouter, HTTPException

from pathlib import Path

from src.recipe_generator import RecipeGenerator
from src.ratings_store import RatingsStore
from src.schemas import (
    RatingRequest,
    RatingResponse,
    RecipeRequest,
    RecipeResponseSchema,
)
from src.utils import parse_ingredients, parse_user_input

logger = logging.getLogger(__name__)

router = APIRouter()
ratings_store = RatingsStore(Path(__file__).resolve().parents[1] / "data" / "ratings.json")


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


@router.post("/api/ratings", response_model=RatingResponse)
def rate_recipe(payload: RatingRequest) -> RatingResponse:
    """
    Rate a generated recipe by recipeId.

    Stores ratings locally (prototype) and returns the aggregated summary.
    """
    try:
        summary = ratings_store.add_rating(payload.recipeId, payload.rating)
        return RatingResponse(recipeId=payload.recipeId, count=summary["count"], avg=summary["avg"])
    except Exception as e:
        logger.exception("Failed to store rating: %s", e)
        raise HTTPException(status_code=500, detail="Failed to store rating") from e


@router.get("/api/ratings/{recipe_id}", response_model=RatingResponse)
def get_rating(recipe_id: str) -> RatingResponse:
    """Get rating summary for a recipeId."""
    summary = ratings_store.get_rating_summary(recipe_id)
    if not summary:
        raise HTTPException(status_code=404, detail="No ratings found for that recipeId")
    return RatingResponse(recipeId=recipe_id, count=summary["count"], avg=summary["avg"])

