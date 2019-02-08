import unittest

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from website.models import *


class AddProductTests(TestCase):
    """ Test the Add Product view and user interactions related to it.

        Author: Sebastian Civarolo

        Methods:
    """

    def test_add_view(self):
        """ Test loading the add product view. """
        user = User.objects.create_user(username="test_user", password="password")
        customer = Customer.objects.create(
            user=user,
            street_address="123 Street St",
            city="Nashville",
            state="TN",
            zipcode="37209",
            phone_number="5555555555"
        )
        self.client.login(username="test_user", password="password")

        response = self.client.get(reverse('website:sell'))
        self.assertEqual(response.status_code, 200)


    # def test_add_product(self):
