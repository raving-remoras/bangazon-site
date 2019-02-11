import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, Order, OrderProduct

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