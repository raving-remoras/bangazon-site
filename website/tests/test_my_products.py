import unittest
from django.test import TestCase, Client
from django.urls import reverse
from ..models import *

class MyProductTest(TestCase):
    """Defines tests for my_product and delete_product views

        Model:
            User
            Customer
            ProductType
            Product
            PaymentType
            Order
            OrderProduct

        Templates:
            my_products.html
            delete_product.html

        Views:
            product_views.py -> my_products
            product_views.py -> delete_product

        Methods:
            setUpClass
            test_my_products
            test_delete_product

        Author:
            Rachel Daniel
            refactored by Kelly Morin
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(MyProductTest, cls).setUpClass()

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

        # create third user who will act as the seller of sold out products
        new_user3 = User.objects.create_user(
            username="test_seller2",
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

        # Create Customer (seller_sold_out)
        customer3 = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user3
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

        # Create second product
        product2 = Product.objects.create(
            seller=customer3,
            product_type=product_type,
            title="Test Product2",
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
            product = product2
        )

    def test_my_products(self):
        """Tests that list of products renders if user has products listed, and that notification of no listed products renders if not"""

        #test that view cannot be accessed if not authenticated
        response = self.client.get(reverse("website:my_products"))
        self.assertFalse(response.content)

        self.client.login(username="test_user", password="secret")

        #test that page now loads but has only a notification of having no products
        response = self.client.get(reverse("website:my_products"))
        self.assertIn("<h4>You haven't listed any Products yet".encode(), response.content)
        self.assertNotIn('class="list-group-item list-group-item-action"'.encode(), response.content)


        self.client.login(username="test_seller", password="secret")

        #test that page now shows product added and has delete btn
        response = self.client.get(reverse("website:my_products"))
        self.assertNotIn("<h4>You haven't listed any Products yet".encode(), response.content)
        self.assertIn('class="list-group-item list-group-item-action"'.encode(), response.content)
        self.assertIn('<h5 class="mb-1">Test Product'.encode(), response.content)
        self.assertIn('class="btn btn-danger float-right" value="Delete"'.encode(), response.content)


        self.client.login(username="test_seller2", password="secret")

        #test that the product no longer has a delete button now that it's sold out
        response = self.client.get(reverse("website:my_products"))
        self.assertNotIn('class="btn btn-danger float-right" value="Delete"'.encode(), response.content)

    def test_delete_product(self):
        """Tests that the delete product form submission performs successful post for customer"""

        self.client.login(username="test_seller", password="secret")

        response = self.client.post(reverse("website:delete_product", args=(1,)))

        self.assertEqual(response.status_code, 302)