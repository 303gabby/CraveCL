import argparse
from meal_generator import MealGenerator
from recipe_manager import RecipeManager
from database import Database
from utils import get_user_input, print_recipe_details, print_history
import os

class CraveCLI:
    def __init__(self):
        self.db = Database()
        self.meal_generator = MealGenerator()
        self.recipe_manager = RecipeManager()
        self.parser = self.setup_parser()

    def setup_parser(self):
        parser = argparse.ArgumentParser(
            description="Crave: Affordable, personalized meals for college students."
        )
        parser.add_argument(
            "--history", action="store_true", help="View your recipe history."
        )
        return parser

    def run(self):
        args = self.parser.parse_args()

        if args.history:
            self.view_history()
            return

        print("Welcome to Crave! Let's cook something delicious and affordable.")

        budget = get_user_input("What's your budget? (e.g., $5, $10, $15): ")
        mood = get_user_input("What mood are you in? (e.g. comforting, healthy, adventurous): ")
        tools = get_user_input("What kitchen tools do you have? (comma-separated, e.g., pan, oven, microwave): ").split(',')
        time = get_user_input("How much time do you want to spend cooking?(e.g 5 mins, 10 mins, etc): ").split(',')
        dietary_restrictions = get_user_input("Any dietary restrictions? (comma-separated, e.g., vegetarian, gluten-free): ").split(',')

        print("\nCrafting your personalized meal idea...")
        meal_idea = self.meal_generator.generate_meal_idea(budget, mood, tools, time,  dietary_restrictions)

        if not meal_idea:
            print("Sorry, I couldn't come up with a meal idea based on your input. Please try again with different preferences.")
            return

        print(f"\nHere's a meal idea for you: {meal_idea}")
        print("Fetching real recipes and details...")
        recipe_data = self.recipe_manager.get_recipe_details(meal_idea, budget, tools, time, dietary_restrictions)

        if not recipe_data:
            print("Couldn't find a suitable recipe from Tasty. Please try a different meal idea or adjust your preferences.")
            return

        print_recipe_details(recipe_data)

        # Store the recipe and user inputs
        self.db.save_meal(
            meal_idea=meal_idea,
            user_inputs={
                "budget": budget,
                "mood": mood,
                "tools": tools,
                "time" : time,
                "dietary_restrictions": dietary_restrictions,
            },
            recipe_data=recipe_data,
        )
        print("\nRecipe saved to your history!")

        while True:
            choice = get_user_input(
                "\nOptions: [s]ave this recipe, [t]ry a variation, [v]iew recipe history, [q]uit: "
            ).lower()
            if choice == 's':
                print("Recipe already saved!")
            elif choice == 't':
                new_meal_idea = get_user_input("What kind of variation would you like? (e.g., 'spicier', 'vegetarian version'): ")
                print("Generating a new variation...")
                variation_idea = self.meal_generator.generate_meal_idea(
                    budget, mood, tools, dietary_restrictions, base_idea=meal_idea, variation_prompt=new_meal_idea
                )
                if variation_idea:
                    print(f"\nNew variation idea: {variation_idea}")
                    variation_recipe_data = self.recipe_manager.get_recipe_details(variation_idea, budget, tools, time, dietary_restrictions)
                    if variation_recipe_data:
                        print_recipe_details(variation_recipe_data)
                        self.db.save_meal(
                            meal_idea=variation_idea,
                            user_inputs={
                                "budget": budget,
                                "mood": mood,
                                "tools": tools,
                                "time": time,
                                "dietary_restrictions": dietary_restrictions,
                            },
                            recipe_data=variation_recipe_data,
                        )
                        print("\nVariation recipe saved to your history!")
                    else:
                        print("Could not find a recipe for this variation.")
                else:
                    print("Could not generate a variation. Please try again.")
            elif choice == 'v':
                self.view_history()
            elif choice == 'q':
                print("Thanks for using Crave! Happy cooking!")
                break
            else:
                print("Invalid option. Please choose 's', 't', 'v', or 'q'.")

    def view_history(self):
        history = self.db.get_meal_history()
        if not history:
            print("Your recipe history is empty.")
            return
        print_history(history)


if __name__ == "__main__":
    cli = CraveCLI()
    cli.run()