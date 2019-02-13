import unittest

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection

class TestAuthViews(TestCase):
    """ Test login, register and logout views.

        Author: Sebastian Civarolo
    """

    def test_login(self):
        """Test login redirects for correct and incorrect logins."""

        user = User.objects.create_user(username="test_user", password="secret")


        response = self.client.post(reverse("website:login"), {"username": ["test_user"], "password": ["secret"]})
        self.assertEqual(response.status_code, 302)

        self.client.logout()

        bad_login = self.client.post(reverse("website:login"), {"username": ["test_user"], "password": ["secrdset"]})
        self.assertIn('Login failed. Your username or password is incorrect.'.encode(), bad_login.content)
