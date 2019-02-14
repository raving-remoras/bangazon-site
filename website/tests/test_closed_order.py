from django.test import TestCase
from ..models import *
from django.urls import reverse

class ClosedOrderTest(TestCase):
    # TODO: Update docstring
    """Tests that a closed order displays correctly on the page.

                Model: Order, Customer, Product, Order_Product, PaymentType

                Template: closed_order.html

                Views: closed_order

                Author: Jase Hackman
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(ClosedOrderTest, cls).setUpClass()

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
        payment_type = PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer = customer
        )

        order = Order.objects.create(
            customer = customer,
            payment_type = payment_type
        )


        order_product = OrderProduct.objects.create(
            order = order,
            product = product
        )


    def test_closed_order_render(self):
        """Tests that a closed order displays properly on the page"""

        self.client.login(username="test_user", password="secret")

        response = self.client.post(reverse('website:closed_order'), {"order_id": 1})

        self.assertIn(
            '<h1 class="mt-3 mb-5">Order Number: BA14793NG-1</h1>'.encode(), response.content
        )
        self.assertIn(
            '<p class="align-self-center align-right m-0">$10</p>'.encode(), response.content
        )
        self.assertIn(
            '<p class="mb-1">Payment Name: '.encode(), response.content
        )