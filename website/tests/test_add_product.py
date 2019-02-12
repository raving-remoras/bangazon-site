import unittest

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection

from website.models import *
from website.forms import ProductForm


class AddProductTests(TestCase):
    """ Test the Add Product view and user interactions related to it.

        Author: Sebastian Civarolo

        Methods:
    """

    def test_add_view(self):
        """ Test loading the add product view with and without a logged in user. """

        user = User.objects.create_user(username="test_user", password="password")
        customer = Customer.objects.create(
            user=user,
            street_address="123 Street St",
            city="Nashville",
            state="TN",
            zipcode="37209",
            phone_number="5555555555"
        )

        # Redirect to login if not logged in.
        not_logged_in_response = self.client.get(reverse("website:sell"))
        self.assertEqual(not_logged_in_response.status_code, 302)

        self.client.login(username="test_user", password="password")

        # Load the view is user is logged in.
        response = self.client.get(reverse("website:sell"))
        self.assertEqual(response.status_code, 200)


    def test_add_product(self):
        """Test that products are successfully added to the database."""

        user = User.objects.create_user(username="test_user", password="password")
        customer = Customer.objects.create(
            user=user,
            street_address="123 Street St",
            city="Nashville",
            state="TN",
            zipcode="37209",
            phone_number="5555555555"
        )
        product_type = ProductType.objects.create(name="Test Product Type")

        form_data = {
            "seller": customer.id,
            "title": "Test Product",
            "description": "Test description",
            "product_type": "1",
            "price": "123",
            "local_delivery": "on",
            "quantity": "123"
        }

        product_form = ProductForm(form_data)

        if product_form.is_valid():

            seller = user.customer.id
            title = form_data["title"]
            description = form_data["description"]
            product_type = form_data["product_type"]
            price = form_data["price"]
            quantity = form_data["quantity"]
            local_delivery = form_data["local_delivery"]

            data = [
                seller, title, description, product_type, price, quantity, local_delivery
            ]

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO website_product
                    (
                        seller_id,
                        title,
                        description,
                        product_type_id,
                        price,
                        quantity,
                        local_delivery
                    )
                    VALUES(
                        %s, %s, %s, %s, %s, %s, %s
                    )
                """, data)
                new_product = cursor.lastrowid

        self.assertEqual(new_product, 1)

    def test_add_photo(self):
        # tests that a photo uploads

        user = User.objects.create_user(username="test_user", password="password")
        customer = Customer.objects.create(
            user=user,
            street_address="123 Street St",
            city="Nashville",
            state="TN",
            zipcode="37209",
            phone_number="5555555555"
        )
        product_type = ProductType.objects.create(name="Test Product Type")

        form_data = {
            "seller": customer.id,
            "title": "Test Product",
            "description": "Test description",
            "product_type": "1",
            "price": "123",
            "local_delivery": "on",
            "quantity": "123",
            "photo": "media_test/small_photo.jpg"
        }

        response= self.client.post(reverse('website:customer_profile'), form_data)
        self.assertEqual(response.status_code, 302)

        form_data2 = {
            "seller": customer.id,
            "title": "Test Product",
            "description": "Test description",
            "product_type": "1",
            "price": "123",
            "local_delivery": "on",
            "quantity": "123",
            "photo": "media_test/large_photo.jpg"
        }

        response2= self.client.post(reverse('website:customer_profile'), form_data2)
        print("HERE", response2.status_code)
        self.assertEqual(response2.status_code, 302)
        self.assertIn('<p class="text-danger">Photo m'.encode(), response.content)


