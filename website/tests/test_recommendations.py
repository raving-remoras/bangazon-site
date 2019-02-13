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

        response = self.client.get(reverse("website:recommend_product"))
        self.assertIn('<input type="text" class="form-control" name="recommended_to"'.encode(), response.content)
        self.assertIn('<textarea class="form-control" rows="3" name="comment"'.encode(), response.content)
        self.assertIn('input class="btn btn-primary" type="submit" value="Send Notification"'.encode(), response.content)