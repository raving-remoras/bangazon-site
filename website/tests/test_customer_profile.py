from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *
from django.test import Client
from django.urls import reverse


class CustomerUserModelTest(TestCase):
    # TODO: Refactor
    """Tests that the user and Customer models post to the database

        Model:
            User
            Customer

        Template:
            customer_profile.html

        Views:
            customer_profile_views.py -> customer_profile

        Author:
            Jase Hackman
            refactored by Kelly Morin
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(CustomerUserModelTest, cls).setUpClass()

        # Create User
        new_user = User.objects.create_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            email="test@test.com",
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

    def test_customer_user_model(self):
        """Tests user and customer models."""

        with self.assertRaises(User.DoesNotExist):
            getUser = User.objects.get(pk=2)
        with self.assertRaises(Customer.DoesNotExist):
            getCustomer = Customer.objects.get(pk=2)

        user = User.objects.create_user(
            username='mrBob',
            first_name="bob",
            last_name="Bobber",
            email="bob@bobsville.com"
        )

        customer = Customer.objects.create(
            user=user,
            street_address="123 South",
            city="Bobville",
            zipcode="12343",
            phone_number=1233211232,
            delete_date=None
        )

        getUser = User.objects.get(pk=2)
        self.assertEqual(user, getUser)
        getCustomer = Customer.objects.get(pk=2)
        self.assertEqual(customer, getCustomer)

    def test_customer_user_profile(self):
        """Tests that a logged in user can access the Customer Profile page"""

        self.client.login(username= "test_user", password = "secret")
        response = self.client.get(reverse("website:customer_profile"))
        self.assertEqual(response.status_code, 200)

    def test_forms(self):
        """Tests that form appear on the page with the correct user info in them."""

        self.client.login(username= "test_user", password = "secret")

        response= self.client.post(reverse('website:customer_profile'),{"edit": "edit"})

        self.assertIn(
            '<input type="text" name="last_name" value="User" '.encode(), response.content
        )
        self.assertIn(
            '<input type="number" name="phone_number" value="1111111111" '.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="street_address" value="123 Test LN" '.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="city" value="Testas" maxlength="100" '.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="state" value="TS" maxlength="100"'.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="zipcode" value="11111" '.encode(), response.content
        )

    def test_edit(self):
        """Tests that the view can edit the user and customer information."""

        self.client.login(username= "test_user", password = "secret")

        userUpdate = {
            "street_address": "125 West",
            "city": "Manhattan",
            "state": "IL",
            "zipcode": "12329",
            "phone_number": 1239541234,
            "last_name": "Smith"
        }

        response= self.client.post(reverse('website:customer_profile'), userUpdate)
        updatedUser = User.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updatedUser.last_name, userUpdate["last_name"])
        self.assertEqual(updatedUser.customer.street_address, userUpdate["street_address"])
        self.assertEqual(updatedUser.customer.city, userUpdate["city"])
        self.assertEqual(updatedUser.customer.state, userUpdate["state"])
        self.assertEqual(updatedUser.customer.zipcode, userUpdate["zipcode"])
        self.assertEqual(updatedUser.customer.phone_number, userUpdate["phone_number"])





