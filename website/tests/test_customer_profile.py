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


class CustomerProfileTest(TestCase):
    def test_forms(self):

        """Tests that form appear on the page with the correct user info in them.

            Model: User, Customer

            Template: customer_profile.html

            Author: Jase Hackman
        """

        user = User.objects.create_user(username='mrBob', password = "ravingramoras", first_name="bob", last_name="Bobber", email="bob@bobsville.com")
        customer = Customer.objects.create(user=user, street_address="123 South", city="Bobville", zipcode="12343", phone_number=1233211232, delete_date=None)
        self.client.login(username= "mrBob", password = "ravingramoras")

        response= self.client.post(reverse('website:customer_profile'),{"edit": "edit"})

        self.assertIn(
            '<input type="text" name="last_name" value="Bobber" maxlength="150" class="textinput textInput" id="id_last_name">'.encode(), response.content
        )
        self.assertIn(
            '<input type="number" name="phone_number" value="1233211232" class="numberinput" required id="id_phone_number">'.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="street_address" value="123 South" maxlength="200" class="textinput textInput" required id="id_street_address">'.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="city" value="Bobville" maxlength="100" class="textinput textInput" required id="id_city">'.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="state" maxlength="100" class="textinput textInput" required id="id_state">'.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="zipcode" value="12343" maxlength="20" class="textinput textInput" required id="id_zipcode">'.encode(), response.content
        )

    def test_edit(self):

         """Tests that the view can edit the user and customer information.

            Model: User, Customer

            Template: customer_profile.html

            Author: Jase Hackman
        """

        user = User.objects.create_user(username='mrBob', password = "ravingramoras", first_name="bob", last_name="Bobber", email="bob@bobsville.com")
        customer = Customer.objects.create(user=user, street_address="123 South", city="Bobville", zipcode="12343", phone_number=1233211232, delete_date=None)
        self.client.login(username= "mrBob", password = "ravingramoras")

        userUpdate = {
            "street_address": "125 West",
            "city": "Manhattan",
            "state": "IL",
            "zipcode": "12329",
            "phone_number": 1239541234,
            "last_name": "Smith"
        }

        response= self.client.post(reverse('website:customer_profile'), userUpdate)
        updatedUser = User.objects.get(pk=user.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updatedUser.id, user.id)
        self.assertEqual(updatedUser.last_name, userUpdate["last_name"])
        self.assertEqual(updatedUser.customer.street_address, userUpdate["street_address"])
        self.assertEqual(updatedUser.customer.city, userUpdate["city"])
        self.assertEqual(updatedUser.customer.state, userUpdate["state"])
        self.assertEqual(updatedUser.customer.zipcode, userUpdate["zipcode"])
        self.assertEqual(updatedUser.customer.phone_number, userUpdate["phone_number"])



