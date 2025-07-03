def get_user_input(prompt):
    """Gets user input with a clear prompt."""
    return input(prompt).strip() 

def print_recipe_details(recipe_data):
    """Prints the detailed recipe information in a user-friendly format."""
    if not recipe_data:
        print("No recipe data to display.")
        return

    print("\n--- Your Personalized Recipe ---")
    print(f"* Meal Name: * {recipe_data.get('title', 'N/A')}")
    print(f"* Servings: * {recipe_data.get('servings', 'N/A')}")
    print(f"* Ready in (minutes): * {recipe_data.get('readyInMinutes', 'N/A')}")
    print(f"* Source URL: * {recipe_data.get('sourceUrl', 'N/A')}")

    print("\n* Ingredients: *")
    if 'extendedIngredients' in recipe_data:
        for ingredient in recipe_data['extendedIngredients']:
            amount = ingredient.get('amount', '')
            unit = ingredient.get('unit', '')
            name = ingredient.get('originalName', '')
            print(f"- {amount} {unit} {name}")
    else:
        print("No ingredients listed.")

    print("\n**Instructions:**")
    if 'instructions' in recipe_data and recipe_data['instructions']:
        print(recipe_data['instructions'])
   
    elif 'analyzedInstructions' in recipe_data and recipe_data['analyzedInstructions']:
        for instruction_set in recipe_data['analyzedInstructions']:
            for step in instruction_set.get('steps', []):
                print(f"Step {step.get('number')}: {step.get('step')}")
    else:
        print("No instructions available.")

    print("\n**Nutritional Information (per serving):**")
    if 'nutrition' in recipe_data and 'nutrients' in recipe_data['nutrition']:
   
        for nutrient in recipe_data['nutrition']['nutrients']:
            if nutrient['name'] in ['Calories', 'Protein', 'Fat', 'Carbohydrates']:
                print(f"- {nutrient['name']}: {nutrient['amount']}{nutrient['unit']}")
    else:
        print("Nutritional information not available.")

    print("---------------------------------\n")

def print_history(history):
    """Prints the user's recipe history."""
    print("\n--- Your Recipe History ---")
    if not history:
        print("No past meals found.")
        return

    for i, meal in enumerate(history): # Loop through each saved meal
        print(f"\nMeal {i+1} (Cooked on: {meal['timestamp']}):")
        print(f"  **Meal Idea:** {meal['meal_idea']}")
        print(f"  **Your Inputs:**")
        for key, value in meal['user_inputs'].items():
            if isinstance(value, list): # If it's a list (like tools or restrictions)
                print(f"    - {key.replace('_', ' ').title()}: {', '.join(value)}")
            else:
                print(f"    - {key.replace('_', ' ').title()}: {value}")
        # Show just the recipe name for history summary
        print(f"  **Recipe Name:** {meal['recipe_data'].get('title', 'N/A')}")
        print("----------------------------")