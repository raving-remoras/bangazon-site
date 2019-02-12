import unittest
from django.test import TestCase, Client
from django.urls import reverse
from ..models import PaymentType, User, Customer, Order


class TestDeletePayment(TestCase):

    def test_hard_delete_payment(self):
        """ Creates user and a payment, and it should hard delete because it has not been used to complete an order.

            Author: Sebastian Civarolo
        """

        new_user = User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password = "secret"
            )

        new_customer = Customer.objects.create(
            street_address = "123 Test LN",
            city = "Testas",
            state=  "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
        )

        self.client.login(username="testuser", password="secret")

        new_payment_type = PaymentType.objects.create(
            name="Test Payment",
            customer=new_customer,
            account_number="1234332177549012"
        )

        # Test loading the current user's payment type delete page
        response = self.client.get(reverse("website:delete_payment_type", args=(1,)))
        self.assertIn("Are you sure you want to delete".encode(), response.content)

        # Test hard delete the current user's unused payment type
        hard_delete_response = self.client.post(reverse("website:delete_payment_type", args=(1,)))
        self.assertEqual(hard_delete_response.status_code, 302)

        # Make sure it's really gone
        with self.assertRaises(PaymentType.DoesNotExist):
            payment_exists = PaymentType.objects.get(pk=1)

    def test_soft_delete_payment(self):
        """ Creates a user, payment type, and an order that uses the payment type. Should soft delete the payment type.

            Author: Sebastian Civarolo
        """

        new_user = User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password = "secret"
            )

        new_customer = Customer.objects.create(
            street_address = "123 Test LN",
            city = "Testas",
            state=  "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
        )

        self.client.login(username="testuser", password="secret")

        new_payment_type = PaymentType.objects.create(
            name="Test Payment",
            customer=new_customer,
            account_number="1234332177549012"
        )

        new_order = Order.objects.create(
            customer = new_customer,
            payment_type = new_payment_type
        )

        # Test loading the current user's payment type delete page
        response = self.client.get(reverse("website:delete_payment_type", args=(1,)))
        self.assertIn("Are you sure you want to delete".encode(), response.content)

        # Test soft delete action
        soft_delete_response = self.client.post(reverse("website:delete_payment_type", args=(1,)))
        self.assertEqual(soft_delete_response.status_code, 302)

        # Test it is there but with a delete_date added
        payment_exists = PaymentType.objects.get(pk=1)
        self.assertIsNotNone(payment_exists.delete_date)

    def test_delete_payment_as_another_user(self):
        """ Creates two users, and user 2 tries to delete user 1's payment type and should be redirected.

            Author: Sebastian Civarolo
        """

        new_user = User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password = "secret"
            )

        new_customer = Customer.objects.create(
            street_address = "123 Test LN",
            city = "Testas",
            state=  "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
        )

        evil_user = User.objects.create_user(
            username = "eviluser",
            first_name = "Test",
            last_name = "User",
            email = "evil@test.com",
            password = "secret"
        )

        evil_customer = Customer.objects.create(
            street_address = "123 Test LN",
            city = "Testas",
            state=  "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = evil_user
        )

        new_payment_type = PaymentType.objects.create(
            name="Test Payment",
            customer=new_customer,
            account_number="1234332177549012"
        )

        self.client.login(username="eviluser", password="secret")

        # Try to load the delete payment page for another user's card
        response = self.client.get(reverse("website:delete_payment_type", args=(1,)))
        card_exists = PaymentType.objects.get(pk=1)

        # Test that the malicious user is redirected back to the user settings page instead of deleting the card
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_payment_type, card_exists)
