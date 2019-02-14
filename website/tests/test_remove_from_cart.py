from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *
from django.test import Client
from django.urls import reverse


class DeleteProductFromCartTest(TestCase):
    """Tests the deletion of a product from a user's cart and the removal of an open order

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
            test_remove_and_delete_open_order
            test_cancel_order

        Author:
            Brendan McCray
            refactored by Kelly Morin
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this case"""

        super(DeleteProductFromCartTest, cls).setUpClass()

        # Create user
        new_user = User.objects.create_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="secret"
        )

        # create second user who will act as the seller of products
        new_user2 = User.objects.create_user(
            username="test_user2",
            first_name="Testx",
            last_name="Userx",
            email="test@testx.com",
            password="secret"
        )

        # create second user who will act as the seller of products
        new_user_seller = User.objects.create_user(
            username="test_user_seller",
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

        # Create Customer
        customer2 = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user2
        )

        customer3 = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user_seller
        )

        # Create product type
        product_type = ProductType.objects.create(
            name = "Test Product Type",
        )

        # Create second product type
        product_type_2 = ProductType.objects.create(
            name = "Test Product Type2",
        )

        # Create product
        product = Product.objects.create(
            seller=customer3,
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
            product_type=product_type_2,
            title="Test Product2",
            description="Not a real product",
            price=10,
            quantity=1,
            delete_date=None
        )

        product3 = Product.objects.create(
            title = "Item 3",
            description = "Something nice",
            price = 25,
            quantity = 1,
            delete_date = None,
            product_type = product_type,
            seller = customer3
        )

        # Create an order with associated products and an available payment type
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

        # Create an order with associated products and an available payment type
        order2 = Order.objects.create(
            customer = customer2,
        )

        payment_type2 = PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer = customer2
        )

        order2_product = OrderProduct.objects.create(
            order = order2,
            product = product
        )

        order2_product2 = OrderProduct.objects.create(
            order = order2,
            product = product2
        )

        order2_product3 = OrderProduct.objects.create(
            order = order2,
            product = product3
        )

    def test_remove_and_delete_open_order(self):
        """Tests that an item can be deleted from the cart, and the last item deleted results in the open order being deleted also"""

        self.client.login(username="test_user", password="secret")

        # Confirm that product title appears in cart
        response = self.client.get(reverse('website:cart'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('<h6 class="mr-auto p-2">Test Product</h6>'.encode(), response.content)

        # confirm that post returns a response of 302
        response = self.client.post(reverse("website:cart"), {"order_product_id": 1, "order_id": 1})
        self.assertEqual(response.status_code, 302)

        # confirm that the open order is also deleted, since only one object was created
        no_order = Order.objects.filter(pk=1)
        self.assertEqual(len(no_order), 0)

    def test_cancel_order(self):
        """Tests that an open order with multiple items will be deleted completely and all order_product join tables are also removed from the database."""


        self.client.login(username="test_user2", password="secret")

        # Confirm that product titles appear in cart
        response = self.client.get(reverse('website:cart'))
        self.assertIn('<h6 class="mr-auto p-2">Test Product</h6>'.encode(), response.content)
        self.assertIn('<h6 class="mr-auto p-2">Test Product2</h6>'.encode(), response.content)
        self.assertIn('<h6 class="mr-auto p-2">Item 3</h6>'.encode(), response.content)


        # confirm that post returns a response of 302
        response = self.client.post(reverse("website:cart"), {"confirmed_deletion": True, "order_id": 2})
        self.assertEqual(response.status_code, 302)

        # confirm that the open order is also deleted, since only one object was created
        no_order = Order.objects.filter(pk=2)
        self.assertEqual(len(no_order), 0)