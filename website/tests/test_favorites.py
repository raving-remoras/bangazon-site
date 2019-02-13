from django.test import TestCase
from ..models import *
from django.urls import reverse

class FavoritesTest(TestCase):
    """Tests that...
            1. product detail page shows 'sold by: {{seller username}} when logged in and logged out
            2. a user can be favorited/unfavorited by a logged in user from the product detail page
            3. the favorites page shows a favorited seller's username with their products

                Model: FavoriteSeller, Product, ProductType, Customer, User

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
        """Tests that product detail page shows 'sold by: {{seller username}} when user is logged out, and there is no 'Unfavorite this seller' button visible on the page (note that the FavoriteSeller join table created in @classMethod indicates that new_user2 is already favorited by new_user)."""

        response = self.client.get(reverse("website:product_details", args=(1,)))
        # check status code of get response
        self.assertEqual(response.status_code, 200)
        # verify that seller's username appears on page
        self.assertIn('<p>Sold by: test_seller</p>'.encode(), response.content)
        # verify that unfavorite button does not appear on page
        self.assertNotIn('<button class="btn btn-danger btn-sm">Unfavorite this Seller</button>'.encode(), response.content)

    def test_view_product_detail_username_logged_in(self):
        """Tests that product detail page shows 'sold by: {{seller username}} when user is not logged in, and that there is an 'Unfavorite this seller' button visible."""

        # log in user
        self.client.login(username="test_user", password="secret")

        response = self.client.get(reverse("website:product_details", args=(1,)))
        # check status code of get response
        self.assertEqual(response.status_code, 200)
        # verify that seller's username appears on page
        self.assertIn('<p>Sold by: test_seller</p>'.encode(), response.content)
        # verify that unfavorite button appears on page
        self.assertIn('<button class="btn btn-danger btn-sm">Unfavorite this Seller</button>'.encode(), response.content)

    def test_unfavorite_user_and_then_favorite_again(self):
        """Tests that
            1. clicking the 'Unfavorite this seller' button performs the desired action of deleting the join table,
            2. that the user then can see a 'Favorite this seller' button, and...
            3. that clicking the 'Favorite this seller' button performs the desired action of creating the join table (i.e. the user will be redirected to the same product detail page, and they will see the 'Unfavorite this seller' button once again).
        """

        # log in user
        self.client.login(username="test_user", password="secret")

        # response indicates user clicks 'unfavorite this seller' button
        response = self.client.post(reverse("website:product_details", args=(1,)), {"current_favorite":True})
        # check status code of post response
        self.assertEqual(response.status_code, 302)

        # verify that the user now sees the 'favorite this seller' button
        response = self.client.get(reverse("website:product_details", args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertIn('<button class="btn btn-success btn-sm">Favorite this Seller</button>'.encode(), response.content)

        # response indicates user clicks 'favorite this seller' button
        response = self.client.post(reverse("website:product_details", args=(1,)))
        self.assertEqual(response.status_code, 302)

        # verify that the user now sees the 'unfavorite this seller' button
        response = self.client.get(reverse("website:product_details", args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertIn('<button class="btn btn-danger btn-sm">Unfavorite this Seller</button>'.encode(), response.content)

    def test_favorites_page_shows_seller_and_products(self):
        """Tests that product detail page shows 'sold by: {{seller username}}"""

        # confirm that a logged out user cannot view the favorites page
        response = self.client.get(reverse("website:favorites"))
        self.assertNotEqual(response.status_code, 200)

        # log in user
        self.client.login(username="test_user", password="secret")

        # confirm that logged in user can see favorited content on favorites page
        response = self.client.get(reverse("website:favorites"))
        self.assertEqual(response.status_code, 200)

        self.assertIn('<h4 class="card-title">test_seller'.encode(), response.content) # seller name
        self.assertIn('<a href="/products/1"'.encode(), response.content) # link to product 1 detail
        self.assertIn('<a href="/products/2"'.encode(), response.content) # link to product 2 detail