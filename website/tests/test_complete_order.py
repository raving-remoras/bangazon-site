import unittest
from django.test import TestCase, Client
from django.urls import reverse
from ..models import *

class CompleteOrderTest(TestCase):
    """Defines tests for payment.py and cart.py views

    Author: Brendan McCray
    Methods:
        test_view_open_order
        test_payment
    """

    def test_view_open_order(self):
        """Tests that the logged in user's cart loads with expected fields if user is authenticated"""

        # test that view cannot be accessed if not authenticated
        response = self.client.get(reverse("website:cart"))
        self.assertFalse(response.content)

        # create new user, log them in, and assign to customer
        new_user= User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password = "password"
            )

        self.client.login(username="testuser", password="password")

        Customer.objects.create(
            street_address = "123 Test Street",
            city = "Test",
            state = "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
            )

        # create an order with associated products and an available payment type
        Order.objects.create(
            customer_id = 1
        )

        PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer_id = 1
        )

        OrderProduct.objects.create(
            order_id = 1,
            product_id = 1
        )

        Product.objects.create(
            title = "Item 1",
            description = "Something nice",
            price = 25,
            quantity = 1,
            delete_date = None,
            product_type_id = 1,
            seller_id = 2
        )

        #test that page now loads
        response = self.client.get(reverse("website:cart"))

        # test that product title appears on page
        self.assertIn('<h6>Item 1</h6>'.encode(), response.content)

    def test_payment(self):
        """Tests that the payment form performs successful update to open order"""

        # create new user, log them in, and assign to customer
        new_user= User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password = "password"
            )

        self.client.login(username="testuser", password="password")

        Customer.objects.create(
            street_address = "123 Test Street",
            city = "Test",
            state = "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
            )

        # create an order with associated products and an available payment type
        Order.objects.create(
            customer_id = 1,
        )

        PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer_id = 1
        )

        OrderProduct.objects.create(
            order_id = 1,
            product_id = 1
        )

        Product.objects.create(
            title = "Item 1",
            description = "Something nice",
            price = 25,
            quantity = 1,
            delete_date = None,
            product_type_id = 1,
            seller_id = 2
        )

        # test submission with complete data
        response = self.client.post(reverse("website:payment"), {"payment_method": 1, "customer_id": 1})
        self.assertEqual(response.status_code, 302)