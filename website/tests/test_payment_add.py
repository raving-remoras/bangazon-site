import unittest
from django.test import TestCase, Client
from django.urls import reverse
from ..models import PaymentType, User, Customer

class PaymentMethodTest(TestCase):
    """Defines tests for Payment Method model and view

    Author: Rachel Daniel
    Methods:
        test_show_form
        test_add_payment
    """

    def test_show_form(self):
        """Tests that the payment type add form page loads with expected fields if user is authenticated"""

        #test that view cannot be accessed if not authenticated
        response = self.client.get(reverse("website:add_payment"))
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

        Customer.objects.create(
            street_address = "123 Test LN",
            city = "Testas",
            state=  "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
            )

        #test that page now loads
        response = self.client.get(reverse("website:add_payment"))
        self.assertIn('<input type="text" name="name"'.encode(), response.content)
        self.assertIn('<input type="number" name="account_number"'.encode(), response.content)
        self.assertIn('<input type="submit" value="submit"'.encode(), response.content)

    def test_add_payment(self):
        """Tests that the add payment form performs successful post for customer"""

        new_user= User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password = "secret"
            )

        self.client.login(username="testuser", password="secret")

        Customer.objects.create(
            street_address = "123 Test LN",
            city = "Testas",
            state=  "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
            )

        #test submitting form with incomplete data
        response = self.client.post(reverse("website:add_payment"), {"account_number": 111111111})

        with self.assertIsNone

        #test submission with complete data
        response = self.client.post(reverse("website:add_payment"), {"name": "Test Payment Type", "account_number": 111111111, "customer_id": 1})

        self.assertEqual(response.status_code, 302)