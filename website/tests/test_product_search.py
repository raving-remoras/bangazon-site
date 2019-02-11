import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection
from ..models import Customer, ProductType, Product

class TestLocalSearch(TestCase):
    """Test class for local delivery search functionality

        Author: Sebastian Civarolo
    """

    def test_local_search(self):
        """Creates a product for delivery in Nashville, and searches for Nashville and Houston."""

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

        seller = user.customer.id
        title = "Test Product"
        description = "test description"
        product_type = "1"
        price = "123"
        quantity = "12"
        local_delivery = "1"
        delivery_city = "Nashville"
        delivery_state = "TN"

        data = [
            seller, title, description, product_type, price, quantity, local_delivery, delivery_city, delivery_state
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
                    local_delivery,
                    delivery_city,
                    delivery_state
                )
                VALUES(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, data)

        response = self.client.post(reverse("website:products"), {"city": ["Nashville"]})

        # check that the product shows up on the results page
        self.assertIn("Showing Local Delivery results".encode(), response.content)
        self.assertIn("Test Product".encode(), response.content)

        # check that the product does not show up when not searching "Nashville"
        response_no_result = self.client.post(reverse("website:products"), {"city": ["Houston"]})
        self.assertIn("Showing Local Delivery results".encode(), response_no_result.content)
        self.assertNotIn("Test Product".encode(), response_no_result.content)

        # check that user's own product does not show up
        self.client.login(username="test_user", password="password")
        response_logged_in = self.client.post(reverse("website:products"), {"city": ["Nashville"]})
        self.assertIn("Showing Local Delivery results".encode(), response_logged_in.content)
        self.assertNotIn("Test Product".encode(), response_logged_in.content)