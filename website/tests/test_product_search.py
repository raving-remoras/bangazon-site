import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection
from ..models import Customer, ProductType, Product


class TestProductSearch(TestCase):
    """Test class for search by product title

        Model:
            Customer
            ProductType
            Product

        Templates:
            product_list.html

        Views:
            product_views.py -> list_products
            product_views.py -> list_search_results

        Methods:
            setUpClass
            test_product_search
            test_local_search

        Author:
            Sebastian Civarolo
            refactored by Kelly Morin
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(TestProductSearch, cls).setUpClass()

        # Create User
        new_user = User.objects.create_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="secret"
        )

        # create second user who will act as the seller of products
        new_user2 = User.objects.create_user(
            username="test_seller",
            first_name="Testx",
            last_name="Userx",
            email="test@testx.com",
            password="secret"
        )

        # Create Customer
        customer = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user
        )

        # Create Customer (seller)
        customer2 = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user2
        )

        # Create product type
        product_type = ProductType.objects.create(
            name = "Some Type",
        )

    def test_product_search(self):
        """Creates a product and search for it"""

        seller_id = 2
        title = "Test Product"
        description = "test description"
        product_type_id = 1
        price = "123"
        quantity = "12"
        local_delivery = "0"

        data = [
            seller_id, title, description, product_type_id, price, quantity, local_delivery
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

        response = self.client.post(reverse("website:products"), {"product_query": ["Test"]})

        # check that the product shows up on the results page
        self.assertIn("Showing search results for".encode(), response.content)
        self.assertIn("Test Product".encode(), response.content)

        # check that the product does not show up when not searching "Test Product"
        response_no_result = self.client.post(reverse("website:products"), {"product_query": ["Houston"]})
        self.assertIn("Showing search results for".encode(), response_no_result.content)
        self.assertNotIn("Test Product".encode(), response_no_result.content)

        # check that user's own product does not show up
        self.client.login(username="test_seller", password="secret")
        response_logged_in = self.client.post(reverse("website:products"), {"product_query": ["Test"]})
        self.assertIn("Showing search results for".encode(), response_logged_in.content)
        self.assertNotIn("Test Product".encode(), response_logged_in.content)

    def test_local_search(self):
        """Creates a product for delivery in Nashville, and searches for Nashville and Houston."""

        seller_id = 2
        title = "Test Product"
        description = "test description"
        product_type_id = 1
        price = "123"
        quantity = "12"
        local_delivery = "1"
        delivery_city = "Nashville"
        delivery_state = "TN"

        data = [
            seller_id, title, description, product_type_id, price, quantity, local_delivery, delivery_city, delivery_state
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
        self.client.login(username="test_seller", password="secret")
        response_logged_in = self.client.post(reverse("website:products"), {"city": ["Nashville"]})
        self.assertIn("Showing Local Delivery results".encode(), response_logged_in.content)
        self.assertNotIn("Test Product".encode(), response_logged_in.content)