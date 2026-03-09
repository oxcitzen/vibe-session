"""CLI entry point for recipe recommendation system."""

import argparse
import json
import logging
import sys
from typing import List

from src.config import Config
from src.recipe_generator import RecipeGenerator
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
