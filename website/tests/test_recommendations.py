import unittest
from django.test import TestCase, Client
from django.urls import reverse
from ..models import *

class MyRecommendationsTest(TestCase):
    """Defines tests for recommendations view

    Author: Rachel Daniel
    Methods:
        test_recommend_template
        test_recommend_product
        test_my_recommendations
        test_delete_recommendation
    """

    def test_recommend_template(self):
        """Tests that the recommend product view loads properly """
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

        response = self.client.get(reverse("website:recommend_product", args=(1, )))
        self.assertIn('<input type="text" class="form-control" name="recommended_to"'.encode(), response.content)
        self.assertIn('<textarea class="form-control" rows="3" name="comment"'.encode(), response.content)
        self.assertIn('input class="btn btn-primary" type="submit" value="Send Notification"'.encode(), response.content)


    def test_recommend_product(self):
        """Tests that the recommend product form submission performs successful post to recommended products"""

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

        #test that the user is redirected back to the product details if they recommend to a correct username
        response = self.client.post(reverse("website:recommend_product", args=(1,)), {"comment": "Test Comment", "recommended_to": "testuser"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/products/1")

        #test that the user is redirected back to the recommendation page if they recommend to an incorrect username
        response = self.client.post(reverse("website:recommend_product", args=(1,)), {"comment": "Test Comment", "recommended_to": "wronguser"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/products/1/recommend")


    def test_my_recommendations(self):
        """Tests that the my recommendations view loads properly with a list item after recommendation """
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

        recommended_product = RecommendedProduct.objects.create(
            comment = "Test Comment",
            product = product,
            recommended_by = customer,
            recommended_to = customer
        )

        response = self.client.get(reverse("website:my_recommendations"))
        self.assertIn('<input type="submit" class="btn-sm btn-danger'.encode(), response.content)
        self.assertIn('<div class="list-group-item list-group-item-action"'.encode(), response.content)


    def test_delete_recommendation(self):
        """Tests that the user gets the correct response after deleting a recommendation """
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

        recommended_product = RecommendedProduct.objects.create(
            comment = "Test Comment",
            product = product,
            recommended_by = customer,
            recommended_to = customer
        )

        response = self.client.post(reverse("website:my_recommendations"),{"Delete": 1})

        self.assertEqual(response.status_code, 302)