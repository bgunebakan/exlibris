from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(cls):
        cls.client = Client()
        cls.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password12345'
        )
        cls.client.login(email='admin@example.com', password='password12345')

        cls.user = get_user_model().objects.create_user(
            email='test@bilaltonga.com',
            password='pass1234',
            name='Test User'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
