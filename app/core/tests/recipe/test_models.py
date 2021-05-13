from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Tag

def sample_user(email="test@gmail.com",password="testpass"):
    return get_user_model().objects.create_user(email,password)


class ModelTests(TestCase):
    """Test all models of recipe app"""

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(user = sample_user(),name = 'Vegan')
        self.assertEqual(str(tag), tag.name)