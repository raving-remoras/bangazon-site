import unittest
import datetime
from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from ..models import PaymentType, User

class PaymentMethodTest(TestCase):
    """Defines tests for Payment Method model and view

    Author: Rachel Daniel
    Methods:
        test_show_form
        test_add_payment
    """

    def test_show_form(self):
        """Tests that the payment type add form page loads with expected fields if user is authenticated"""

        new_user = User.object.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com"
            ),
        response = self.client.get(reverse("website:add_payment"))
        print("CONTENT", response.content)
        self.assertIn('<input type="text" name="name"'.encode(), response.content)
        self.assertIn('<input type="number" name="account_number"'.encode(), response.content)
        self.assertIn('<input type="submit" value="submit"'.encode(), response.content)