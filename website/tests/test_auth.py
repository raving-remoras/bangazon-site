import unittest

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection

class TestAuthViews(TestCase):
    # TODO: Update docstring
    """ Test login, register and logout views.

        Author: Sebastian Civarolo
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each of the tests in this class"""

        super(TestAuthViews, cls).setUpClass()

        # Create user
        new_user = User.objects.create_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="secret"
        )


    def test_login(self):
        """Test login redirects for correct and incorrect logins."""


        response = self.client.post(reverse("website:login"), {"username": ["test_user"], "password": ["secret"]})
        self.assertEqual(response.status_code, 302)

        self.client.logout()

        bad_login = self.client.post(reverse("website:login"), {"username": ["test_user"], "password": ["secrdset"]})
        self.assertIn('Login failed. Your username or password is incorrect.'.encode(), bad_login.content)
