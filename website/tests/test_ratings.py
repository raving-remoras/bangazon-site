import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, Order, OrderProduct, PaymentType

class TestRatingSystem(TestCase):
    """ Tests adding ratings and displaying ratings around the site.

            Model:
                Customer
                User
                ProductType
                Product
                Order
                OrderProduct
                PaymentType

            Templates:
                product_detail.html
                closed_order.html
                my_products.html

            Views:
                product_views.py -> product_details
                closed_order_views.py -> closed_order
                product_views.py -> my_products

            Methods:
                setUpClass
                test_add_rating

            Author:
                Sebastian Civarolo
                refactored by Kelly Morin
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(TestRatingSystem, cls).setUpClass()

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

        payment_type = PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer = customer
        )

        order = Order.objects.create(
            customer = customer,
        )

        order_product = OrderProduct.objects.create(
            order = order,
            product = product
        )

    def test_add_rating(self):
        """Tests that a closed order displays properly on the page"""

        self.client.login(username="test_user", password="secret")

        # test submitting a new rating from order page
        response = self.client.post(reverse("website:closed_order"), {"order_id": 1, "rating": 4, "orderproduct_id": 1})
        self.assertEqual(response.status_code, 200)
        # self.assertIn('id="rating-4-1" name="rating" checked>'.encode(), response.content)

        # test the rating showing up on product detail view
        product_detail_response = self.client.get(reverse("website:product_details", args=(1,)))
        self.assertIn('<span class="badge badge-success">Avg Rating: 4.0 / 5 from 1 customers</span>'.encode(), product_detail_response.content)

        self.client.login(username="test_seller", password="secret")
        # test the rating showing on seller's my products view
        seller_view_response = self.client.get(reverse("website:my_products"))
        self.assertIn('<span class="badge badge-warning">Avg Rating: 4.0 / 5 from 1 customers</span>'.encode(), seller_view_response.content)

