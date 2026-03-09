"""API request/response schemas."""

from pydantic import BaseModel, Field

from src.models import RecipeResponse


class RecipeRequest(BaseModel):
    """Request body for generating recipes."""

    ingredients: str = Field(
        ...,
        min_length=1,
        description="Comma-separated list of ingredients (e.g., 'pasta, garlic, butter')",
    )


# Re-export response schema for clarity at API layer.
RecipeResponseSchema = RecipeResponse

