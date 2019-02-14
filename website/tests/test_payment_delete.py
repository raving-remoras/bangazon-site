import unittest
from django.test import TestCase, Client
from django.urls import reverse
from ..models import PaymentType, User, Customer, Order


class TestDeletePayment(TestCase):
    """[summary]

    Model:
        PaymentType
        User
        Customer
        Order

    Templates:
        payment_delete.html
        customer_profile.html

    Views:
        payment_views.py -> delete_payment_type

    Methods:
        setUpClass
        test_hard_delete_payment
        test_soft_delete_payment
        test_delete_payment_as_another_user

    Author:
        Sebastian Civarolo
        refactored by Kelly Morin
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(TestDeletePayment, cls).setUpClass()

        # create user
        new_user = User.objects.create_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="secret"
        )

        # create second user
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

        # Create Customer
        customer2 = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user2
        )

        payment_type = PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer = customer
        )

        payment_type2 = PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer = customer
        )

        payment_type3 = PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer = customer
        )

        order = Order.objects.create(
            customer = customer,
            payment_type = payment_type2
        )

    def test_hard_delete_payment(self):
        """ Creates user and a payment, and it should hard delete because it has not been used to complete an order.

            Author: Sebastian Civarolo
        """

        self.client.login(username="test_user", password="secret")

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

        self.client.login(username="test_user", password="secret")

        # Test loading the current user's payment type delete page
        response = self.client.get(reverse("website:delete_payment_type", args=(2,)))
        self.assertIn("Are you sure you want to delete".encode(), response.content)

        # Test soft delete action
        soft_delete_response = self.client.post(reverse("website:delete_payment_type", args=(2,)))
        self.assertEqual(soft_delete_response.status_code, 302)

        # Test it is there but with a delete_date added
        payment_exists = PaymentType.objects.get(pk=2)
        self.assertIsNotNone(payment_exists.delete_date)

    def test_delete_payment_as_another_user(self):
        """ Creates two users, and user 2 tries to delete user 1's payment type and should be redirected.

            Author: Sebastian Civarolo
        """
        self.client.login(username="customer2", password="secret")

        # Try to load the delete payment page for another user's card
        response = self.client.get(reverse("website:delete_payment_type", args=(3,)))
        card_exists = PaymentType.objects.get(pk=3)

        # Test that the malicious user is redirected back to the user settings page instead of deleting the card
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(card_exists)
