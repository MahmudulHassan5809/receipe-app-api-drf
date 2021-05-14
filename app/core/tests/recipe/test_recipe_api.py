from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Recipe,Tag,Ingredient

from recipe.serializers import RecipeSerializer,RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Return recipe detail url """
    return reverse('recipe:recipe-detail',args=[recipe_id])

def create_user(**params):
    return get_user_model().objects.create_user(**params)

def sample_tag(user,name='Main Course'):
    """Create and return a sample tag """
    return Tag.objects.create(user=user,name=name)


def sample_ingredient(user,name='Main Course'):
    """Create and return a sample ingredient """
    return Ingredient.objects.create(user=user,name=name)

def sample_recipe(user,**params):
    """Create and return a recipe"""
    defaults = {
       'title' : 'Sample Recipe',
       'time_minutes' : 10,
       'price' : 5.00 
    }
    defaults.update(params)

    return Recipe.objects.create(user=user,**defaults)


class PublicIngredientsApiTest(TestCase):
    """Test the publicly available recipe api"""

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """Test that login is required for retrieving recipe"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the authorized user recipe API"""

    def setUp(self):
        self.user = create_user(
            email = "test@gmail.com",
            password="testpass",
            name="Test Name"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_recipes(self):
        """Test retrieving recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes,many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_retrieve_user_ingredients_only(self):
        """Test that recipes returned are for the authenticated user"""
        user2 = create_user(
            email = "other@gmail.com",
            password="testpass",
            name="Other Name"
        )

        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes,many = True)
        
        
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data, serializer.data)
    
    def test_view_recipe_detail(self):
        """test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)

        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
    

    # def test_create_ingredient_successful(self):
    #     """Test creating a new ingredients"""
    #     payload = {'name' : 'Test Ingredient'}
    #     self.client.post(INGREDIENTS_URL,payload)

    #     exists = Ingredient.objects.filter(
    #         user = self.user,
    #         name = payload['name']
    #     ).exists()

    #     self.assertTrue(exists)

    # def test_create_ingredient_invalid(self):
    #     """Test creating a new ingredient with invalid payload"""
    #     payload = {'name' : ''}
    #     res = self.client.post(INGREDIENTS_URL,payload)
    #     self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)