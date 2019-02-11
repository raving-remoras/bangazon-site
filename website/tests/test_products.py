import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, Order, OrderProduct, PaymentType

class ProductTest(TestCase):

    def test_list_products(self):
        """Test case verifies that the products are listed when the navbar's 'shop' link is clicked"""

        new_seller = Customer.objects.create(
            user = User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com"
            ),
            street_address = "1112 Some Dr.",
            city = "City",
            state = "TN",
            zipcode = "1122334",
            phone_number = 1112233
        )

        new_product_type = ProductType.objects.create(
            id = 3,
            name = "Some Product",
        )

        new_product = Product.objects.create(
            seller = new_seller,
            product_type = new_product_type,
            title = "Test Product",
            description = "This is a product that should make your life better",
            price = 11,
            quantity = 15,
            local_delivery = 0
        )

        # Issue a GET request
        response = self.client.get(reverse('website:products'))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 1 product
        self.assertEqual(len(response.context['products']),1)

        # Check that the product title appears in the rendered HTML content
        self.assertIn(new_product.title.encode(), response.content)


    def test_get_product_detail(self):
        """Test case verifies that a specific product details are rendered when a specific product is selected from the product list"""

        new_seller = Customer.objects.create(
            user = User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com"
            ),
            street_address = "1112 Some Dr.",
            city = "City",
            state = "TN",
            zipcode = "1122334",
            phone_number = 1112233
        )

        new_product_type = ProductType.objects.create(
            id = 3,
            name = "Some Product",
        )

        new_product = Product.objects.create(
            seller = new_seller,
            product_type = new_product_type,
            title = "Test Product",
            description = "This is a product that should make your life better",
            price = 11,
            local_delivery = 0,
            quantity = 15
        )

        response = self.client.get(reverse('website:product_details', args=(1,)))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Check that the product type is in the HTML response content
        self.assertEqual(response.context['product_details'], new_product)

        # Product title appears in HTML response content
        self.assertIn(new_product.title.encode(), response.content)

    def test_add_to_cart(self):

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

        # Confirm that the post returns a response of 302
        response = self.client.get(reverse("website:add_to_cart", args=(1,)))
        self.assertEqual(response.status_code, 302)