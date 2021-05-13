from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Tag,Ingredient,Recipe

def sample_user(email="test@gmail.com",password="testpass"):
    return get_user_model().objects.create_user(email,password)


class ModelTests(TestCase):
    """Test all models of recipe app"""

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(user = sample_user(),name = 'Vegan')
        self.assertEqual(str(tag), tag.name)
    
    def test_ingredient_str(self):
        """Test the Ingredient string representation"""
        ingredient = Ingredient.objects.create(user = sample_user(),name = 'Cucumber')
        self.assertEqual(str(ingredient), ingredient.name)
    

    def test_recipe_str(self):
        """Test the Recipe string representation"""
        recipe = Recipe.objects.create(
            user = sample_user(),
            title = 'Steak and mashroo sauce',
            time_minutes = 5,
            price = 5.00
        )
        self.assertEqual(str(recipe), recipe.title)