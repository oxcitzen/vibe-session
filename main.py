"""CLI entry point for recipe recommendation system."""

import argparse
import json
import logging
import sys
from typing import List
from pathlib import Path

from src.config import Config
from src.recipe_generator import RecipeGenerator
from src.ratings_store import RatingsStore
from src.utils import parse_user_input

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def display_recipes(recipe_response) -> None:
    """
    Display recipes in formatted JSON.
    
    Args:
        recipe_response: RecipeResponse object to display
    """
    # Convert to dict and pretty print
    output = recipe_response.model_dump(mode='json')
    print("\n" + "="*60)
    print("RECIPE RECOMMENDATIONS")
    print("="*60 + "\n")
    print(json.dumps(output, indent=2, ensure_ascii=False))
    print("\n" + "="*60)


def prompt_for_ratings(recipe_response) -> None:
    """
    Prompt user to rate recipes (1-5) after generation and store locally.
    """
    store = RatingsStore(Path(__file__).resolve().parent / "data" / "ratings.json")
    print("\nRate the recipes (1-5). Press Enter to skip.\n")

    for recipe in recipe_response.recipes:
        rid = getattr(recipe, "recipeId", None)
        name = getattr(recipe, "name", "Recipe")
        if not rid:
            continue

        while True:
            raw = input(f'Rating for "{name}" (id: {rid}) [1-5 or Enter]: ').strip()
            if raw == "":
                break
            try:
                rating = int(raw)
                if rating < 1 or rating > 5:
                    raise ValueError("out of range")
                summary = store.add_rating(rid, rating)
                print(f"Saved. Avg: {summary['avg']} ({summary['count']})\n")
                break
            except Exception:
                print("Please enter a number from 1 to 5, or press Enter to skip.")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Generate recipe recommendations based on ingredients",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "pasta, garlic, butter, parmesan"
  python main.py "chicken, rice, vegetables"
  python main.py "tomato, basil, mozzarella, olive oil"

Note: In PowerShell, always use quotes around the ingredients string.
        """
    )
    
    parser.add_argument(
        "ingredients",
        type=str,
        nargs='?',  # Optional to provide custom error message
        help="Comma-separated list of ingredients (e.g., 'pasta, garlic, butter')"
    )
    
    args = parser.parse_args()
    
    # Check if ingredients were provided
    if not args.ingredients:
        parser.print_help()
        print("\n" + "="*60)
        print("ERROR: Ingredients are required!")
        print("="*60)
        print("\nUsage examples:")
        print('  python main.py "pasta, garlic, butter, parmesan"')
        print('  python main.py "chicken, rice, vegetables"')
        print("\nNote: In PowerShell, use quotes around the ingredients string.")
        sys.exit(1)
    
    ingredients_str = args.ingredients
    
    try:
        # Parse ingredients
        logger.info("Parsing ingredients...")
        ingredients, dietary_restrictions = parse_user_input(ingredients_str)
        print(f"\nInput ingredients: {', '.join(ingredients)}")
        if dietary_restrictions:
            print(f"Dietary restrictions: {', '.join(dietary_restrictions)}")
        print("Generating recipe recommendations...\n")
        
        # Generate recipes
        generator = RecipeGenerator()
        recipe_response = generator.generate_recipes(
            ingredients,
            dietary_restrictions=dietary_restrictions,
        )
        
        # Display results
        display_recipes(recipe_response)
        prompt_for_ratings(recipe_response)
        
        logger.info("Recipe generation completed successfully")
        
    except ValueError as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
