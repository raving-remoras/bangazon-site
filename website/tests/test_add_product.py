import unittest

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection

from website.models import *
from website.forms import ProductForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.contrib.staticfiles import finders


class AddProductTests(TestCase):
    """Tests add product view and user interactions related to it
            Model:
                Product
                ProductType
                Customer

            Templates:
                product/create.html
                product_details.html

            Views:
                sell_views.py -> sell_product

            Author:
                Sebastian Civarolo
                Jase Hackman
                Kelly Morin

    """
    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(AddProductTests, cls).setUpClass()

        # create user
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

        # Create customer
        customer = Customer.objects.create(
            user= new_user,
            street_address="123 Street St",
            city="Nashville",
            state="TN",
            zipcode="37209",
            phone_number="5555555555"
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
            name = "Test Product Type",
        )

    def test_add_view(self):
        """ Test loading the add product view with and without a logged in user. """

        # Redirect to login if not logged in.
        not_logged_in_response = self.client.get(reverse("website:sell"))
        self.assertEqual(not_logged_in_response.status_code, 302)

        self.client.login(username="test_user", password="secret")

        # Load the view is user is logged in.
        response = self.client.get(reverse("website:sell"))
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        """Test that products are successfully added to the database."""

        form_data = {
            "seller_id": 2,
            "title": "Test Product",
            "description": "Test description",
            "product_type_id": 1,
            "price": "123",
            "local_delivery": "on",
            "quantity": "123"
        }

        product_form = ProductForm(form_data)

        if product_form.is_valid():

            seller_id = form_data["seller_id"]
            title = form_data["title"]
            description = form_data["description"]
            product_type = form_data["product_type_id"]
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
        """Tests that a small photo will be uploaded and a large photo will not be uploaded"""

        user = User.objects.create_user(username="test_user2", password="password")
        customer = Customer.objects.create(
                user=user,
                street_address="123 Street St",
                city="Nashville",
                state="TN",
                zipcode="37209",
                phone_number="5555555555"
            )
        product_type = ProductType.objects.create(name="Test Product Type")

        self.client.login(username="test_user2", password="password")

        # test that a small photo url will post to the database
        with open("media_test/small_photo.jpg", "rb") as np:

            form_data3 = {
                "seller": customer.id,
                "title": "Test Product",
                "description": "Test description",
                "product_type": "1",
                "price": "123",
                "quantity": "123",
                "photo": np
            }
            response = self.client.post(reverse('website:sell'), form_data3)
            product = Product.objects.get(pk=1)
            self.assertEqual(response.status_code, 302)

        # test that a large photo will not be in the data base and will have a redirect
        with open("media_test/large_photo.jpg", "rb") as fp:

            form_data2 = {
                "seller": customer.id,
                "title": "Test Product",
                "description": "Test description",
                "product_type": "1",
                "price": "123",
                "quantity": "123",
                "photo": fp
            }

            response3= self.client.post(reverse('website:sell'), form_data2)
            self.assertEqual(response3.status_code, 200)
            with self.assertRaises(Product.DoesNotExist):
                product2 = Product.objects.get(pk=2)

    def test_add_negative_quantity(self):
        """Test that negative quantites cannot be submitted"""

        # Log in seller
        self.client.login(username="test_seller", password="secret")

        # Issue a GET request
        response = self.client.get(reverse("website:sell"))

        # Check that the response is 200
        self.assertEqual(response.status_code, 200)

        # Submit fake form with negative quantity
        form_data = {
            "seller_id": 2,
            "title": "Test Product",
            "description": "Test description",
            "product_type_id": 1,
            "price": "123",
            "local_delivery": "on",
            "quantity": "-12"
        }

        product_form = ProductForm(form_data)

        # Check that form validation throws an error
        self.assertFalse(product_form.is_valid())

        # Check that the form validation specifically throws an error on quantity and provides the correct error message
        self.assertEquals(product_form.errors['quantity'], ['Ensure this value is greater than or equal to 0.'])

    def test_add_excessive_price(self):
        """Test that prices over 10,000 cannot be submitted"""

        # Log in seller
        self.client.login(username="test_seller", password="secret")

        # Issue a GET request
        response = self.client.get(reverse("website:sell"))

        # Check that the response is 200
        self.assertEqual(response.status_code, 200)

        # Submit fake form with price greater than 10,000
        form_data = {
            "seller_id": 2,
            "title": "Test Product",
            "description": "Test description",
            "product_type_id": 1,
            "price": "1230000",
            "local_delivery": "on",
            "quantity": "12"
        }

        product_form = ProductForm(form_data)

        # Check that form validation throws an error
        self.assertFalse(product_form.is_valid())

        # Check that the form validation specifically throws an error on quantity and provides the correct error message
        self.assertEquals(product_form.errors['price'], ['Ensure this value is less than or equal to 10000.'])

