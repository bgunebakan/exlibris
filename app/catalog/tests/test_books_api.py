from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book

from catalog.serializers import BookSerializer


BOOKS_URL = reverse('catalog:book-list')


class PublicBookApiTests(TestCase):
    """Test the publicly avaliable books API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""

        res = self.client.get(BOOKS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBooksApiTests(TestCase):
    """Test the private books API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_book_list(self):
        """Test retrieving a list of books"""

        Book.objects.create(user=self.user, name='Romeo and Juliet')
        Book.objects.create(user=self.user, name='Lord of the Rings')

        res = self.client.get(BOOKS_URL)

        books = Book.objects.all().order_by('-name')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_books_limited_to_user(self):
        """Test that books for the authenticated user are returned"""

        user2 = get_user_model().objects.create_user(
            'other@example.com',
            'testpass'
        )

        Book.objects.create(user=user2, name="Angela's Ashes")
        book = Book.objects.create(user=self.user, name='Alice in Wonderland')

        res = self.client.get(BOOKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], book.name)

    def test_create_book_successful(self):
        """Test create a new book"""

        payload = {'name': 'Alice in Wonderland'}
        self.client.post(BOOKS_URL, payload)

        exists = Book.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_book_invalid(self):
        """Test creating invalid book fails"""

        payload = {'name': ''}
        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
