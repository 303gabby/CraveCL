import requests
import os 
import json 

class RecipeManager:
    def __init__(self):
   
        self.api_key = "e8f840284cmsha965fb8d670029dp1b8bafjsn58931215bd6f" 
        self.api_host = "tasty.p.rapidapi.com"        

        self.base_url = f"https://{self.api_host}/recipes" 

        self.headers = {
            "X-RapidAPI-Host": self.api_host,
            "X-RapidAPI-Key": self.api_key
        }

       
      

    def get_recipe_details(self, meal_idea, budget, tools, time, dietary_restrictions):
        """
        Fetches recipe details from Tasty API based on the meal idea and user preferences.
        """
        search_url = f"https://{self.api_host}/recipes/list"
        search_params = {
            "from": "0", 
            "size": "1", 
            "q": meal_idea 
        }

        print(f"Searching Tasty for: '{meal_idea}'")

        try:
            response = requests.get(search_url, headers=self.headers, params=search_params)
            response.raise_for_status() 
            data = response.json()

            if data and data.get('results'):
                first_result = data['results'][0]
                recipe_id = first_result.get('id')
                recipe_name = first_result.get('name')

                if recipe_id:
                    print(f"Found recipe: '{recipe_name}' (ID: {recipe_id}). Fetching details...")
                    return self._get_recipe_by_id(recipe_id)
                else:
                    print("No ID found for the first recipe result from Tasty.")
                    return None
            else:
                print(f"No suitable recipes found on Tasty for '{meal_idea}'.")
                return None

        except requests.exceptions.RequestException as e:
            if e.response is not None:
                print(f"Error fetching recipe from Tasty API: {e.response.status_code} - {e.response.text}")
            else:
                print(f"Error fetching recipe from Tasty API: {e}")
            return None
        except json.JSONDecodeError as e:
       
            print(f"Error decoding JSON response from Tasty API: {e}. Raw response: {response.text if 'response' in locals() else 'No response object.'}")
            return None

    def _get_recipe_by_id(self, recipe_id):
        """
        Fetches detailed recipe information for a given recipe ID from Tasty API.
        """
        detail_url = f"https://{self.api_host}/recipes/get-more-info"
        detail_params = {
            "id": str(recipe_id) 
        }

        try:
            response = requests.get(detail_url, headers=self.headers, params=detail_params)
            response.raise_for_status()
            recipe_data = response.json()

            if recipe_data:
                return self._parse_tasty_recipe(recipe_data)
            else:
                print(f"No detailed information found for recipe ID: {recipe_id}")
                return None
        except requests.exceptions.RequestException as e:
            if e.response is not None:
                print(f"Error fetching detailed recipe by ID from Tasty API: {e.response.status_code} - {e.response.text}")
            else:
                print(f"Error fetching detailed recipe by ID from Tasty API: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response from Tasty API for ID {recipe_id}: {e}. Raw response: {response.text if 'response' in locals() else 'No response object.'}")
            return None

    def _parse_tasty_recipe(self, tasty_data):
        """
        Parses the raw JSON data from Tasty API into a consistent format for Crave.
        """
        parsed_recipe = {
            'title': tasty_data.get('name', 'N/A'),
            'servings': tasty_data.get('num_servings', 'N/A'),
            'readyInMinutes': tasty_data.get('total_time_minutes', 'N/A'),
            'sourceUrl': tasty_data.get('canonical_url', 'N/A'),
            'image': tasty_data.get('thumbnail_url', None),
            'extendedIngredients': [],
            'instructions': '',
            'nutrition': {'nutrients': []}
        }

        # Ingredients
        if 'sections' in tasty_data:
            for section in tasty_data['sections']:
                if 'components' in section:
                    for component in section['components']:
                        
                        ingredient_name = component.get('raw_text', '')
                        if ingredient_name:
                            parsed_recipe['extendedIngredients'].append({
                                'originalName': ingredient_name,
                                'amount': '', 
                                'unit': ''
                            })

        # Instructions
        if 'instructions' in tasty_data:
            steps_list = []
            for i, instruction_step in enumerate(tasty_data['instructions']):
                display_text = instruction_step.get('display_text', '').strip()
                if display_text:
                    steps_list.append(f"Step {i+1}: {display_text}")
            parsed_recipe['instructions'] = "\n".join(steps_list)
        else:
            parsed_recipe['instructions'] = "No detailed instructions available."

        # Nutrition
        if 'nutrition' in tasty_data and tasty_data['nutrition'].get('has_nutrition_info'):
            nutrition_info = tasty_data['nutrition']
            
            nutrition_map = {
                'calories': 'Calories',
                'protein': 'Protein',
                'fat': 'Fat',
                'carbohydrates': 'Carbohydrates',
                'fiber': 'Fiber',
                'sugar': 'Sugar'
            }
            for tasty_key, display_name in nutrition_map.items():
                if tasty_key in nutrition_info:
                    parsed_recipe['nutrition']['nutrients'].append({
                        'name': display_name,
                        'amount': nutrition_info[tasty_key],
                        'unit': 'kcal' if tasty_key == 'calories' else 'g'
                    })

        return parsed_recipe

