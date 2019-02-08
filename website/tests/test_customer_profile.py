from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *
from django.test import Client
from django.urls import reverse



class CustomerUserModelTest(TestCase):
    """Tests that the user and Customer models post to the database

        Model:User, Customer

        Template:

        Author: Jase Hackman
    """
    def test_customer_user_model(self):
        """Tests user and customer models.

            Model: User, Customer

            Template:

            Author: Jase Hackman
        """

        with self.assertRaises(User.DoesNotExist):
            getUser = User.objects.get(pk=1)
        with self.assertRaises(Customer.DoesNotExist):
            getCustomer = Customer.objects.get(pk=1)
        user = User.objects.create_user(username='mrBob', first_name="bob", last_name="Bobber", email="bob@bobsville.com")
        customer = Customer.objects.create(user=user, street_address="123 South", city="Bobville", zipcode="12343", phone_number=1233211232, delete_date=None)
        getUser = User.objects.get(pk=1)
        self.assertEqual(user, getUser)
        getCustomer = Customer.objects.get(pk=1)
        self.assertEqual(customer, getCustomer)

    def test_customer_user_profile(self):
        """Tests that a logged in user can access the Customer Profile page

            Model: User, Customer

            Template: customer_profile.html

            Author: Jase Hackman
        """

        user = User.objects.create_user(username='mrBob', password = "ravingramoras", first_name="bob", last_name="Bobber", email="bob@bobsville.com")
        customer = Customer.objects.create(user=user, street_address="123 South", city="Bobville", zipcode="12343", phone_number=1233211232, delete_date=None)
        self.client.login(username= "mrBob", password = "ravingramoras")
        response = self.client.get(reverse("website:customer_profile"))
        self.assertEqual(response.status_code, 200)
