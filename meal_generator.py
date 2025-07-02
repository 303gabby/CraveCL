import google.generativeai as genai 
import os 

class MealGenerator:
    def __init__(self):
       
        genai.configure(api_key="AIzaSyChb6h4vtkkc-maCYtNA7UJ1MhhU9ePasM")
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_meal_idea(self, budget, mood, tools, time, dietary_restrictions, base_idea=None, variation_prompt=None):
        """
        Generates a tailored meal idea based on user inputs.
        """
        # This is the "prompt" we send to the AI. 
        prompt = (
            f"As a culinary assistant for college students, suggest a personalized meal idea "
            f"considering the following:\n"
            f"- Budget: {budget}\n"
            f"- Mood: {mood}\n"
            f"- Kitchen tools available: {', '.join(tools)}\n"
            f"- Time: {time}\n"
            f"- Dietary restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}\n"
        )
        # If the user wants a variation, we add that to the prompt
        if base_idea and variation_prompt:
            prompt += f"Based on '{base_idea}', suggest a variation that is '{variation_prompt}'.\n"

        prompt += "Please provide only the name of the meal, without any additional text or formatting."

        try:
            # Send the prompt to the AI and get a response
            response = self.model.generate_content(prompt)
            # We just want the text part of the AI's answer
            meal_idea = response.text.strip()
            return meal_idea
        except Exception as e:
            # If something goes wrong, print an error
            print(f"Error generating meal idea with Google GenAI: {e}")
            return None