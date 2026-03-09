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

    dietaryRestrictions: str | None = Field(
        default=None,
        description=(
            "Optional comma-separated dietary restrictions (e.g., 'vegan, gluten-free'). "
            "Alternatively, append to ingredients with '|' like: "
            "'pasta, garlic | vegan, gluten-free'."
        ),
    )


# Re-export response schema for clarity at API layer.
RecipeResponseSchema = RecipeResponse

