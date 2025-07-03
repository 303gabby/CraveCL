import unittest
from unittest.mock import MagicMock, patch
from meal_suggestion import CreateMeal

class TestCreateMeal(unittest.TestCase):
    
    # Test 1: generate_meal_idea returns a meal name
    @patch("meal_generator.genai.GenerativeModel")
    def test_generate_meal_idea(self, mock_model):
        fake_response = MagicMock()
        fake_response.text = "Mac and Cheese"
        mock_model.return_value.generate_content.return_value = fake_response

        gen = CreateMeal()
        result = gen.generate_meal_idea(
            budget="$5",
            mood="comforting",
            tools=["microwave"],
            time=["10 mins"],
            dietary_restrictions=["vegetarian"]
        )

        self.assertEqual(result, "Mac and Cheese")

    # Test 2: generate_full_recipe returns a full recipe text
    @patch("meal_generator.genai.GenerativeModel")
    def test_generate_full_recipe(self, mock_model):
        fake_response = MagicMock()
        fake_response.text = "Here is your recipe..."
        mock_model.return_value.generate_content.return_value = fake_response

        gen = CreateMeal()
        result = gen.generate_full_recipe(
            meal_idea="Mac and Cheese",
            budget="$5",
            tools=["microwave"],
            time=["10 mins"],
            dietary_restrictions=["vegetarian"]
        )

        self.assertEqual(result, "Here is your recipe...")

 
    @patch("meal_generator.genai.GenerativeModel")
    def test_generate_meal_with_variation(self, mock_model):
        fake_response = MagicMock()
        fake_response.text = "Spicy Mac and Cheese"
        mock_model.return_value.generate_content.return_value = fake_response

        gen = CreateMeal()
        result = gen.generate_meal_idea(
            budget="$5",
            mood="spicy",
            tools=["microwave"],
            time=["10 mins"],
            dietary_restrictions=["vegetarian"],
            base_idea="Mac and Cheese",
            variation_prompt="spicier"
        )

        self.assertEqual(result, "Spicy Mac and Cheese")

if __name__ == "__main__":
    unittest.main()

