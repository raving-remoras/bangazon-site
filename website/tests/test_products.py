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

    def product_category_view(self):
        """Test case verifies that all product categories and their associated products are rendered when the product category affordance is selected from the navbar"""
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
            name = "Some Product",
        )

        new_product_type_2 = ProductType.objects.create(
            name = "Some Product",
        )

        new_product = Product.objects.create(
            seller = new_seller,
            product_type = new_product_type,
            title = "Test Product",
            description = "This is a product that should make your life better",
            price = 11,
            quantity = 15
        )

        new_product_2 = Product.objects.create(
            seller = new_seller,
            product_type = new_product_type_2,
            title = "Test Product",
            description = "This is a product that should make your life better",
            price = 11,
            quantity = 15
        )

        response = self.client.get(reverse('website:product_categories'))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 2 product types
        self.assertEqual(len(response.context['product_categories']),2)

        # Check that the product type is in the HTML response content
        self.assertEqual(response.context['product_categories'], new_product_type)
        self.assertEqual(response.context['product_categories'], new_product_type_2)
        self.assertEqual(response.context['product_categories'], new_product)
        self.assertEqual(response.context['product_categories'], new_product_2)

        # Product title appears in HTML response content
        self.assertIn(new_product.title.encode(), response.content)
        self.assertIn(new_product_2.title.encode(), response.content)
        self.assertIn(new_product_type.name.encode(), response.content)
        self.assertIn(new_product_type_2.name.encode(), response.content)

    def test_add_to_cart(self):
        """Test case verifies that a product is added to the database on an open order when a user selects the add to cart button from the product detail page"""

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

    def product_by_category(self):
        """Test case verifies that all products associated with a specific category display when the product category is requested"""

        new_seller = Customer.objects.create(
            user = User.objects.create_user(
            username = "testuser",
            first_name = "Test",
            last_name = "User",
            email = "test@test.com",
            password="password"
            ),
            street_address = "1112 Some Dr.",
            city = "City",
            state = "TN",
            zipcode = "1122334",
            phone_number = 1112233
        )

        new_customer = Customer.objects.create(
            user = User.objects.create_user(
            username = "someuser",
            first_name = "Some",
            last_name = "User",
            email = "user@test.com",
            password="password1"
            ),
            street_address = "1234 Some Dr.",
            city = "City",
            state = "TN",
            zipcode = "1122334",
            phone_number = 1112233
        )

        new_product_type = ProductType.objects.create(
            name = "Product Type 1",
        )

        new_product_type_2 = ProductType.objects.create(
            name = "Product Type 2",
        )

        new_product = Product.objects.create(
            seller = new_seller,
            product_type = new_product_type,
            title = "New Product 1",
            description = "This is a product that should make your life better",
            price = 11,
            quantity = 15
        )

        new_product_2 = Product.objects.create(
            seller = new_seller,
            product_type = new_product_type_2,
            title = "A Product Name",
            description = "This is a product that should make your life better",
            price = 11,
            quantity = 15
        )

        # Guest user, searching for product category 1
        response = self.client.get(reverse('website:product_by_category', args=(1,)))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Check that new_product is the only product that shows in the query
        self.assertIn(new_product.title.encode(), response.content)
        self.assertNotIn(new_product_2.title.encode(), response.content)

        # Check that the quantity is in the HTML response content
        self.assertEqual(response.context['product_by_category'], new_product)
        self.assertNotEqual(response.context['product_by_category'], new_product_2)

        # Log In user that is not the seller, check that the products not created by the user do show up
        self.client.login(username="someuser", password="password")
        # Search for product category 1
        response_non_seller = self.client.get(reverse('website:product_by_category', args=(1,)))
        self.assertEqual(response_non_seller.status_code, 200)
        self.assertIn(new_product.title.encode(), response_non_seller.content)
        self.assertNotIn(new_product_2.title.encode(), response_non_seller.content)
        # Search for product category 2
        response_non_seller_2 = self.client.get(reverse('website:product_by_category', args=(2,)))
        self.assertIn(new_product_2.title.encode(), response_non_seller_2.content)
        self.assertNotIn(new_product_2.title.encode(), response_non_seller_2.content)

        # Check that user's own product does not show up
        self.client.login(username="testuser", password="password")
        # Search for product category 1
        response_logged_in = self.client.get(reverse('website:product_by_category', args=(1,)))
        self.assertEqual(response_logged_in.status_code, 200)
        self.assertNotIn(new_product.title.encode(), response_logged_in.content)
        self.assertNotIn(new_product_2.title.encode(), response_logged_in.content)
        # Search for product category 2
        response_logged_in_2 = self.client.get(reverse('website:product_by_category', args=(2,)))
        self.assertNotIn(new_product.title.encode(), response_logged_in_2.content)
        self.assertNotIn(new_product_2.title.encode(), response_logged_in_2.content)
