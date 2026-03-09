"""Shared utilities for CLI and web API."""

from typing import List


def parse_ingredients(input_string: str) -> List[str]:
    """
    Parse comma-separated ingredients string into a list.

    Normalizes by trimming whitespace and lowercasing.

    Args:
        input_string: Comma-separated string of ingredients

    Returns:
        List of normalized ingredient names
    """
    if not input_string or not input_string.strip():
        raise ValueError("No ingredients provided")

    ingredients = [
        ingredient.strip().lower()
        for ingredient in input_string.split(",")
        if ingredient.strip()
    ]

    if not ingredients:
        raise ValueError("No valid ingredients found")

    if len(ingredients) > 20:
        raise ValueError("Too many ingredients (maximum 20 allowed)")

    return ingredients

