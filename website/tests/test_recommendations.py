import unittest
from django.test import TestCase, Client
from django.urls import reverse
from ..models import *

class MyRecommendationsTest(TestCase):
    """Defines tests for recommendations view

            Model:
                Customer
                User
                Product
                ProductType
                RecommendedProduct

            Templates:
                recommend_product.html
                my_recommendations.html

            Views:
                recommendation_views.py -> recommend_product
                recommendation_views.py -> my_recommendations

            Methods:
                test_recommend_template
                test_recommend_product
                test_my_recommendations
                test_delete_recommendation

            Author:
                Rachel Daniel
                refactored by Kelly Morin
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(MyRecommendationsTest, cls).setUpClass()

        # Create User
        new_user = User.objects.create_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="secret"
        )

        # create second user who will act as the seller of products
        new_user2 = User.objects.create_user(
            username="test_seller",
            first_name="Testx",
            last_name="Userx",
            email="test@testx.com",
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

        # Create Customer (seller)
        customer2 = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user2
        )

        # Create product type
        product_type = ProductType.objects.create(
            name = "Test Product Type",
        )

        # Create product
        product = Product.objects.create(
            seller=customer2,
            product_type=product_type,
            title="Test Product",
            description="Not a real product",
            price=10,
            quantity=1,
            delete_date=None
        )

        recommended_product = RecommendedProduct.objects.create(
            comment = "Test Comment",
            product = product,
            recommended_by = customer2,
            recommended_to = customer
        )


    def test_recommend_template(self):
        """Tests that the recommend product view loads properly """

        self.client.login(username="test_user", password="secret")

        response = self.client.get(reverse("website:recommend_product", args=(1, )))
        self.assertIn('<input type="text" class="form-control" name="recommended_to"'.encode(), response.content)
        self.assertIn('<textarea class="form-control" rows="3" name="comment"'.encode(), response.content)
        self.assertIn('input class="btn btn-primary" type="submit" value="Send Notification"'.encode(), response.content)


    def test_recommend_product(self):
        """Tests that the recommend product form submission performs successful post to recommended products"""

        self.client.login(username="test_user", password="secret")

        #test that the user is redirected back to the product details if they recommend to a correct username
        response = self.client.post(reverse("website:recommend_product", args=(1,)), {"comment": "Test Comment", "recommended_to": "test_user"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/products/1")

        #test that the user is redirected back to the recommendation page if they recommend to an incorrect username
        response = self.client.post(reverse("website:recommend_product", args=(1,)), {"comment": "Test Comment", "recommended_to": "wronguser"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/products/1/recommend")


    def test_my_recommendations(self):
        """Tests that the my recommendations view loads properly with a list item after recommendation """

        self.client.login(username="test_user", password="secret")

        response = self.client.get(reverse("website:my_recommendations"))
        self.assertIn('<input type="submit" class="btn-sm btn-danger'.encode(), response.content)
        self.assertIn('<div class="list-group-item list-group-item-action"'.encode(), response.content)


    def test_delete_recommendation(self):
        """Tests that the user gets the correct response after deleting a recommendation """

        self.client.login(username="test_user", password="secret")

        response = self.client.post(reverse("website:my_recommendations"),{"Delete": 1})

        self.assertEqual(response.status_code, 302)