from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *
from django.test import Client
from django.urls import reverse

class DeleteProductFromCartTest(TestCase):
    """Tests the deletion of a product from a user's cart and the removal of an open order

    Author: Brendan McCray
    Methods: test_remove_and_delete_open_order

    """

    def test_remove_and_delete_open_order(self):
        """Tests that an item can be deleted from the cart, and the last item deleted results in the open order being deleted also"""

        # create new user, log them in, and assign to customer
        new_user= User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password = "password"
            )

        self.client.login(username="testuser", password="password")

        Customer.objects.create(
            street_address = "123 Test Street",
            city = "Test",
            state = "TS",
            zipcode = "11111",
            phone_number = "1111111111",
            user = new_user
            )

        # create an order with associated products and an available payment type
        Order.objects.create(
            customer_id = 1,
        )

        PaymentType.objects.create(
            name = "User's credit card",
            account_number = 123456789,
            delete_date = None,
            customer_id = 1
        )

        OrderProduct.objects.create(
            order_id = 1,
            product_id = 1
        )

        product = Product.objects.create(
            title = "Item 1",
            description = "Something nice",
            price = 25,
            quantity = 1,
            delete_date = None,
            product_type_id = 1,
            seller_id = 2
        )

        # Confirm that product title appears in cart
        response = self.client.get(reverse('website:cart'))
        self.assertIn(product.title.encode(), response.content)

        # confirm that post returns a response of 302
        response = self.client.post(reverse("website:cart"), {"order_product_id": 1, "order_id": 1})
        self.assertEqual(response.status_code, 302)

        # confirm that the open order is also deleted, since only one object was created
        no_order = Order.objects.filter(pk=1)
        self.assertEqual(len(no_order), 0)