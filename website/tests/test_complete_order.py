import unittest
from django.test import TestCase, Client
from django.urls import reverse
from ..models import *

class CompleteOrderTest(TestCase):
    """Defines tests for payment.py and cart.py views

        Model:
            Customer
            Product
            ProductType
            Order
            OrderProduct
            PaymentType

        Templates:
            cart.html

        Views:
            cart.py -> cart

        Methods:
            setUpClass
            test_view_open_order
            test_payment

        Author:
            Brendan McCray
            refactored by Kelly Morin
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(CompleteOrderTest, cls).setUpClass()

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

        # create an order with associated products and an available payment type
        order = Order.objects.create(
            customer = customer,
        )

        payment_type = PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer = customer
        )

        order_product = OrderProduct.objects.create(
            order = order,
            product = product
        )

    def test_view_open_order(self):
        """Tests that the logged in user's cart loads with expected fields if user is authenticated"""

        # test that view cannot be accessed if not authenticated
        response = self.client.get(reverse("website:cart"))
        self.assertFalse(response.content)

        self.client.login(username="test_user", password="secret")

        #test that page now loads
        response = self.client.get(reverse("website:cart"))

        # test that product title appears on page
        self.assertIn('<h6 class="mr-auto p-2">Test Product</h6>'.encode(), response.content)

    def test_payment(self):
        """Tests that the payment form performs successful update to open order"""

        self.client.login(username="testuser", password="password")

        # test submission with complete data
        response = self.client.post(reverse("website:payment"), {"payment_method": 1, "customer_id": 1})
        self.assertEqual(response.status_code, 302)