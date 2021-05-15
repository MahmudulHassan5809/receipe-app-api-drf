from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Ingredient,Recipe

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicIngredientsApiTest(TestCase):
    """Test the publicly available ingredients api"""

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """Test that login is required for retrieving ingredients"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the authorized user ingredients API"""

    def setUp(self):
        self.user = create_user(
            email = "test@gmail.com",
            password="testpass",
            name="Test Name"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_ingredients(self):
        """Test retrieving ingredients"""
        Ingredient.objects.create(user=self.user,name="Vegan")
        Ingredient.objects.create(user=self.user,name="Dessert")

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients,many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_retrieve_user_ingredients_only(self):
        """Test that ingredients returned are for the authenticated user"""
        user2 = create_user(
            email = "other@gmail.com",
            password="testpass",
            name="Other Name"
        )

        Ingredient.objects.create(user=user2,name="Fruity")
        ingredient = Ingredient.objects.create(user = self.user, name = "Comfort Food")

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],ingredient.name)
    
    def test_create_ingredient_successful(self):
        """Test creating a new ingredients"""
        payload = {'name' : 'Test Ingredient'}
        self.client.post(INGREDIENTS_URL,payload)

        exists = Ingredient.objects.filter(
            user = self.user,
            name = payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating a new ingredient with invalid payload"""
        payload = {'name' : ''}
        res = self.client.post(INGREDIENTS_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    
    def test_retrieve_ingredients_assigned_to_recipe(self):
        """Test filtering ingredients by those assigned to recipes"""
        ingredient1 = Ingredient.objects.create(user = self.user , name = "Breakfast")
        ingredient2 = Ingredient.objects.create(user = self.user , name = "Lunch")
        recipe = Recipe.objects.create(
            title = 'Cordiander eggs on toast',
            time_minutes = 10,
            price = 5.00,
            user = self.user
        )

        recipe.ingredients.add(ingredient1)
        res = self.client.get(INGREDIENTS_URL,{'assigned_only' : 1})

        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)

        self.assertIn(serializer1.data , res.data)
        self.assertNotIn(serializer2.data , res.data)

