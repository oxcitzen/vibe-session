"""Pydantic models for recipe data validation."""

from typing import List
from pydantic import BaseModel, Field, field_validator


class Nutrition(BaseModel):
    """Nutritional information for a recipe."""
    
    calories: int = Field(..., description="Calories per serving", gt=0)
    protein: str = Field(..., description="Protein content with unit (e.g., '12g')")
    carbs: str = Field(..., description="Carbohydrate content with unit (e.g., '60g')")
    
    @field_validator("protein", "carbs")
    @classmethod
    def validate_nutrition_string(cls, v: str) -> str:
        """Validate nutrition string format."""
        if not isinstance(v, str) or len(v.strip()) == 0:
            raise ValueError("Nutrition value must be a non-empty string")
        return v.strip()


class Recipe(BaseModel):
    """Recipe model with all required fields."""
    
    name: str = Field(..., description="Name of the recipe", min_length=1)
    ingredients: List[str] = Field(..., description="List of ingredients", min_length=1)
    instructions: List[str] = Field(..., description="Step-by-step cooking instructions", min_length=1)
    cookingTime: str = Field(..., description="Estimated cooking time (e.g., '20 minutes')")
    difficulty: str = Field(..., description="Difficulty level: Easy, Medium, or Hard")
    nutrition: Nutrition = Field(..., description="Nutritional information")
    dietaryRestrictions: List[str] = Field(
        default_factory=list,
        description="Dietary restrictions this recipe complies with (e.g., 'vegan', 'gluten-free')",
    )
    
    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        """Validate difficulty level."""
        valid_levels = ["Easy", "Medium", "Hard"]
        if v not in valid_levels:
            raise ValueError(f"Difficulty must be one of: {', '.join(valid_levels)}")
        return v
    
    @field_validator("ingredients", "instructions")
    @classmethod
    def validate_list_not_empty(cls, v: List[str]) -> List[str]:
        """Validate that lists are not empty."""
        if not v or len(v) == 0:
            raise ValueError("List cannot be empty")
        return [item.strip() for item in v if item.strip()]

    @field_validator("dietaryRestrictions")
    @classmethod
    def validate_dietary_restrictions(cls, v: List[str]) -> List[str]:
        """Normalize dietary restrictions."""
        if not v:
            return []
        normalized = [str(item).strip().lower() for item in v if str(item).strip()]
        # Deduplicate while preserving order
        seen = set()
        out: List[str] = []
        for item in normalized:
            if item not in seen:
                seen.add(item)
                out.append(item)
        return out


class RecipeResponse(BaseModel):
    """Response model containing multiple recipe suggestions."""
    
    recipes: List[Recipe] = Field(..., description="List of recipe suggestions", min_length=2, max_length=3)
    
    @field_validator("recipes")
    @classmethod
    def validate_recipe_count(cls, v: List[Recipe]) -> List[Recipe]:
        """Validate recipe count is between 2 and 3."""
        if len(v) < 2 or len(v) > 3:
            raise ValueError("Must provide exactly 2-3 recipe suggestions")
        return v
