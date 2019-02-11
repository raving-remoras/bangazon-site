import unittest
from django.test import TestCase, Client
from django.urls import reverse
from ..models import *

class MyProductTest(TestCase):
    """Defines tests for my_product and delete_product views

    Author: Rachel Daniel
    Methods:
        test_my_products
        test_delete_product
    """

    def test_my_products(self):
        """Tests that list of products renders if user has products listed, and that notification of no listed products renders if not"""


        #test that view cannot be accessed if not authenticated
        response = self.client.get(reverse("website:my_products"))
        self.assertFalse(response.content)

        #create new user, log them in, and assign to customer
        new_user= User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password = "secret"
            )

        self.client.login(username="testuser", password="secret")

        customer = Customer.objects.create(
            street_address = "123 Test LN",
            city = "Testas",
            state =  "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
            )


        #test that page now loads but has only a notification of having no products
        response = self.client.get(reverse("website:my_products"))
        self.assertIn("<h4>You haven't listed any Products yet".encode(), response.content)
        self.assertNotIn('class="list-group-item list-group-item-action"'.encode(), response.content)

        product_type = ProductType.objects.create(
            name = "Test Type"
        )

        product = Product.objects.create(
            seller = customer,
            product_type = product_type,
            title = "Test Product",
            description = "Not a real product",
            price = 10,
            quantity = 1,
            delete_date = None
        )

        #test that page now shows product added and has delete btn
        response = self.client.get(reverse("website:my_products"))
        self.assertNotIn("<h4>You haven't listed any Products yet".encode(), response.content)
        self.assertIn('class="list-group-item list-group-item-action"'.encode(), response.content)
        self.assertIn('<h5 class="mb-1">Test Product'.encode(), response.content)
        self.assertIn('class="btn btn-danger float-right" value="Delete"'.encode(), response.content)

        payment_type = PaymentType.objects.create(
            name = "Test Payment Type",
            account_number = 111111111,
            customer = customer
        )

        order = Order.objects.create(
            customer = customer,
            payment_type = payment_type
        )

        OrderProduct.objects.create(
            order = order,
            product = product
        )

        #test that the product no longer has a delete button now that it's sold out
        response = self.client.get(reverse("website:my_products"))
        self.assertNotIn('class="btn btn-danger float-right" value="Delete"'.encode(), response.content)

    def test_delete_product(self):
        """Tests that the delete product form submission performs successful post for customer"""

        new_user= User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password = "secret"
            )

        self.client.login(username="testuser", password="secret")

        customer = Customer.objects.create(
            street_address = "123 Test LN",
            city = "Testas",
            state =  "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
            )

        product_type = ProductType.objects.create(
            name = "Test Type"
        )

        product = Product.objects.create(
            seller = customer,
            product_type = product_type,
            title = "Test Product",
            description = "Not a real product",
            price = 10,
            quantity = 1,
            delete_date = None
        )

        order = Order.objects.create(
            customer = customer,
            payment_type = None
        )

        OrderProduct.objects.create(
            order = order,
            product = product
        )

        response = self.client.post(reverse("website:delete_product", args=(1,)))

        self.assertEqual(response.status_code, 302)