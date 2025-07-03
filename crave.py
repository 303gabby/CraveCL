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


    def _handle_new_recipe_generation(self):
        """
        Handles the process of asking for user inputs, generating a meal idea,
        fetching/generating a recipe, displaying it, and saving it.
        Returns True if a recipe was successfully generated and displayed, False otherwise.
        """
        budget = get_user_input("\nWhat's your budget? (e.g., $5, $10, $15):")
        mood = get_user_input("\nWhat mood are you in? (e.g. comforting, healthy, adventurous):")
        tools = get_user_input("\nWhat kitchen tools do you have? (comma-separated, e.g., pan, oven, microwave):").split(',')
        time = get_user_input("\nHow much time do you want to spend cooking?(e.g 5 mins, 10 mins, etc): ").split(',')
        dietary_restrictions = get_user_input("\nAny dietary restrictions? (comma-separated, e.g., vegetarian, gluten-free):").split(',')

        print("\nCrafting your personalized meal idea...")
        meal_idea = self.meal_generator.generate_meal_idea(budget, mood, tools, time,  dietary_restrictions)

        if not meal_idea:
            print("\nSorry, I couldn't come up with a meal idea based on your input. Please try again with different preferences.")
            return False, None, None, None, None, None 

        print(f"\nHere's a meal idea for you: {meal_idea}")
        print("\nFetching real recipes and details...")
        recipe_data = self.recipe_manager.get_recipe_details(meal_idea, budget, tools, time, dietary_restrictions)

        if not recipe_data:
            print("\nCouldn't find a suitable recipe. Please try a different meal idea or adjust your preferences.")
            return False, None, None, None, None, None 

        print_recipe_details(recipe_data)

        # Store the recipe and user inputs (only if successful)
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
      
        return True, meal_idea, budget, mood, tools, time, dietary_restrictions, recipe_data
  
    def run(self):
        args = self.parser.parse_args()

        if args.history:
            self.view_history()
            return

        print("\nWelcome to Crave! Let's cook something delicious and affordable.")
        print("\nHow it Works")
        print("\nYou will be asked 5 questions: - what your budget is, your mood, kitchen tools available to you, the amount of time you want to spend making your dish and your dietary restrictions.")
        print("\nFrom there we will generate a meal suited to your tastes using the GenAI and Tasty API.") 
        print("\nIf the suggested meal/dish isn't found on Tasty, have no fear!. Our GenAI will take the lead and generate a recipe for you.We hope you enjoy what we have to offer. \n Bon Appetit!")

        while True:
            initial_choice = get_user_input(
                "\nOptions: Start a new recipe [n], View recipe history [v], Quit [q]: "
            ).lower()

            if initial_choice == 'n':
              
                recipe_success, meal_idea, budget, mood, tools, time, dietary_restrictions, recipe_data = self._handle_new_recipe_generation()

                # If a recipe was successfully generated, then show the post-recipe options
                if recipe_success:
                  
                    while True:
                        choice = get_user_input(
                            "\nOptions: save this recipe [enter s], try a variation [enter t], view recipe history[enter v], start new recipe [enter n], quit [enter q]: "
                        ).lower()
                        if choice == 's':
                            print("Recipe already saved!")
                        elif choice == 't':
                            new_meal_idea = get_user_input("What kind of variation would you like? (e.g., 'spicier', 'vegetarian version'): ")
                            print("Generating a new variation...")
                            variation_idea = self.meal_generator.generate_meal_idea(
                                budget, mood, tools, time, dietary_restrictions, base_idea=meal_idea, variation_prompt=new_meal_idea
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
                                    print("\nCould not find a recipe for this variation.")
                            else:
                                print("\nCould not generate a variation. Please try again.")
                        elif choice == 'v':
                            self.view_history()
                        elif choice == 'n':
                            break 
                        elif choice == 'q':
                            print("\nThanks for using Crave! Happy cooking!")
                            return 
                        else:
                            print("\nInvalid option. Please choose 's', 't', 'v', 'n', or 'q'.")
             

            elif initial_choice == 'v':
                self.view_history()
                continue
            elif initial_choice == 'q':
                print("\nThanks for using Crave! Happy cooking!")
                return
            else:
                print("\nInvalid option. Please choose 'n', 'v', or 'q'.")
        

    def view_history(self):
        history = self.db.get_meal_history()
        if not history:
            print("\nYour recipe history is empty.")
            return
        print_history(history)


if __name__ == "__main__":
    cli = CraveCLI()
    cli.run()