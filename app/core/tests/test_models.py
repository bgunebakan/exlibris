from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@example.com', password='test1234'):
    """Create a test user"""

    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating new user with an email is successful"""

        email = 'test@example.com'
        password = 'TEST123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        email = 'test@EXAMPLE.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new superuser"""

        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""

        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Literature'
        )

        self.assertEqual(str(tag), tag.name)

    def test_book_str(self):
        """Test the book string respresentation"""

        book = models.Book.objects.create(
            user=sample_user(),
            name='Harry Potter'
        )

        self.assertEqual(str(book), book.name)
