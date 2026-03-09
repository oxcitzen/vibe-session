"""Shared utilities for CLI and web API."""

import re
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


def parse_user_input(input_string: str) -> tuple[List[str], List[str]]:
    """
    Parse user input that may include dietary restrictions at the end.

    Supported formats:
    - "pasta, garlic, butter, parmesan"
    - "pasta, garlic, butter, parmesan | vegan, gluten-free"
    - "pasta, garlic, butter, parmesan ; vegan, gluten-free"

    Returns:
        (ingredients_list, dietary_restrictions_list)
    """
    if not input_string or not input_string.strip():
        raise ValueError("No ingredients provided")

    raw = input_string.strip()

    # Split on first '|' or ';' (common separators for "ingredients | restrictions")
    parts = re.split(r"\s*[|;]\s*", raw, maxsplit=1)
    ingredients_part = parts[0].strip()
    restrictions_part = parts[1].strip() if len(parts) > 1 else ""

    ingredients = parse_ingredients(ingredients_part)

    dietary_restrictions: List[str] = []
    if restrictions_part:
        dietary_restrictions = [
            r.strip().lower()
            for r in restrictions_part.split(",")
            if r.strip()
        ]

    # Deduplicate while preserving order
    seen = set()
    deduped: List[str] = []
    for r in dietary_restrictions:
        if r not in seen:
            seen.add(r)
            deduped.append(r)

    return ingredients, deduped

