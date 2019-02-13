from django.test import TestCase
from ..models import *
from django.urls import reverse

class FavoritesTest(TestCase):
    """Tests that...
            1. product detail page shows 'sold by: {{seller username}} when logged in and logged out
            2. a user can be favorited/unfavorited by a logged in user from the product detail page
            3. the favorites page shows a favorited seller's username with their products

                Model: FavoriteSeller

                Templates: product_detail.html, favorites.html

                Views: product_views.py -> product_detail, favorites

                Author: Brendan McCray
    """

    @classmethod
    def setUpClass(cls):
        """creates instances of databse objects before running each test in this class"""
        super(FavoritesTest, cls).setUpClass()
        # create user
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
        # create customer
        customer = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user
        )
        # create customer (seller)
        customer2 = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user2
        )
        # identify product type for testing (insignificant in this test    beyond placeholder)
        product_type = ProductType.objects.create(
            name="Test Type"
        )
        # create two products
        product = Product.objects.create(
            seller=customer2,
            product_type=product_type,
            title="Test Product",
            description="Not a real product",
            price=10,
            quantity=1,
            delete_date=None
        )
        product2 = Product.objects.create(
            seller=customer2,
            product_type=product_type,
            title="Test Product2",
            description="Not a real product",
            price=10,
            quantity=1,
            delete_date=None
        )
        favorite_seller = FavoriteSeller.objects.create(
            user_id=1,
            seller_id=2
        )

    def test_view_product_detail_seller_username_while_logged_out(self):
        """Tests that product detail page shows 'sold by: {{seller username}} when user is logged in"""

        response = self.client.get(reverse("website:product_details", args=(1,)))
        self.assertIn('<p>Sold by: test_seller</p>'.encode(), response.content)

    def test_view_product_detail_username_logged_in(self):
        """Tests that product detail page shows 'sold by: {{seller username}} when user is not logged in"""

        # log in user
        self.client.login(username="test_user", password="secret")

        response = self.client.get(reverse("website:product_details", args=(1,)))
        self.assertIn('<p>Sold by: test_seller</p>'.encode(), response.content)

    # def test_favorite_user(self):
    #     """Tests that product detail page shows 'sold by: {{seller username}}"""

    # def test_unfavorite_user(self):
    #     """Tests that product detail page shows 'sold by: {{seller username}}"""

    # def test_favorites_page(self):
    #     """Tests that product detail page shows 'sold by: {{seller username}}"""