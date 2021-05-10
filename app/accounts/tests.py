from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class AccountTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successfull"""
        email = "test@gmail.com"
        password = "bd@12345"

        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test the email for new user is normalized"""
        email = 'test@GMAIL.com'
        user = get_user_model().objects.create_user(email,'bd@12345')
        self.assertEqual(user.email,email.lower())

    
    def test_new_user_valid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'bd@12345')

    def test_create_new_super_user(self):
        email = "test@gmail.com"
        password = "bd@12345"
        
        user = get_user_model().objects.create_superuser(
            email = email,
            password = password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)