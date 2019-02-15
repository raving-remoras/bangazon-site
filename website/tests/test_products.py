import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, Order, OrderProduct, PaymentType

class ProductTest(TestCase):
    """Tests that:
            1. Guest users can see all products
            2. Logged in sellers only see products they did not create
            3. All product details are available when a product is selected
            4. Product categories and their associated products are rendered when 'product categories' is selected from the navbar
            5. The cart renders correctly and the add to cart functionality works
            6. When selecting a specific product category the associated products are displayed for both guest and logged in non-sellers
            7. When selecting a specific product category, the non-owned associated products are displayed for logged in sellers

            Model:
                Customer
                Product
                ProductType
                Order
                OrderProduct
                PaymentType

            Templates:
                product_list.html
                product_detail.html
                product_category.html
                product_by_category.html
                cart.html

            Views:
                product_category_views.py -> product_categories
                product_category_views.py -> product_by_category
                product_views.py -> list_products
                product_views.py -> product_details
                product_views.py -> add_to_cart
                cart.py -> cart

            Methods:
                setUpClass
                test_list_products
                test_list_products_logged_in
                test_get_product_detail
                test_product_category_view
                test_add_to_cart
                test_product_by_category_guest
                test_product_by_category_logged_in_user
                test_product_by_category_logged_in_seller


            Author:
                Kelly Morin
                Brendan McCray
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(ProductTest, cls).setUpClass()

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

        # Create second product type
        product_type_2 = ProductType.objects.create(
            name = "Test Product Type2",
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
            seller=customer2,
            product_type=product_type_2,
            title="Test Product2",
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

    def test_list_products(self):
        """Test case verifies that the products are listed when the navbar's 'shop' link is clicked"""

        # Issue a GET request
        response = self.client.get(reverse('website:products'))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Check that the context contains 2 products
        self.assertEqual(len(response.context['products']),2)

        # Check that the product title appears in the rendered HTML content
        self.assertIn('<h5 class="card-title mb-0">Test Product</h5>'.encode(), response.content)
        self.assertIn('<h5 class="card-title mb-0">Test Product2</h5>'.encode(), response.content)

    def test_list_products_logged_in(self):
        """Test case verifies that when the seller is logged in and selects the navbar's 'shop' link, their products will not be displayed"""

        # Log in seller
        self.client.login(username="test_seller", password="secret")

        # Issue a GET request
        response = self.client.get(reverse('website:products'))

        # Check that the response is 200
        self.assertEqual(response.status_code, 200)

        # Check that the logged in user does not recieve any products to view because the only products available are the ones they have for sale
        self.assertEqual(len(response.context['products']),0)

        # Check that the product title appears in the rendered HTML content
        self.assertNotIn('<h5 class="card-title mb-0">Test Product</h5>'.encode(), response.content)
        self.assertNotIn('<h5 class="card-title mb-0">Test Product2</h5>'.encode(), response.content)

    def test_get_product_detail(self):
        """Test case verifies that a specific product details are rendered when a specific product is selected from the product list"""

        response = self.client.get(reverse('website:product_details', args=(1,)))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Product title appears in HTML response content
        self.assertIn('<h1>Test Product</h1>'.encode(), response.content)
        self.assertNotIn('<h1>Test Product2</h1>'.encode(), response.content)

    def test_product_category_view(self):
        """Test case verifies that all product categories and their associated products are rendered when the product category affordance is selected from the navbar"""

        response = self.client.get(reverse('website:product_categories'))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 2 product types
        self.assertEqual(len(response.context['product_categories']),2)

        # Product title appears in HTML response content
        self.assertIn('<h6 class="mb-1">Test Product</h6>'.encode(), response.content)
        self.assertIn('<h6 class="mb-1">Test Product2</h6>'.encode(), response.content)
        self.assertIn('<h4 class="card-title">Test Product Type <p class="badge badge-primary ml-2">1</p></h4>'.encode(), response.content)
        self.assertIn('<h4 class="card-title">Test Product Type2 <p class="badge badge-primary ml-2">1</p></h4>'.encode(), response.content)

    def test_add_to_cart(self):
        """Test case verifies that a product is added to the database on an open order when a user selects the add to cart button from the product detail page"""

        # Log the user in that is not the seller
        self.client.login(username="test_user", password="secret")

        # Confirm that product title appears in cart
        response = self.client.get(reverse('website:cart'))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Ensure that the cart displays product title, but not the title for product2
        self.assertIn('<h6 class="mr-auto p-2">Test Product</h6>'.encode(), response.content)
        self.assertNotIn('<h6 class="mr-auto p-2">Test Product2</h6>'.encode(), response.content)

        # Confirm that the post returns a response of 302
        response = self.client.get(reverse("website:add_to_cart", args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_product_by_category_guest(self):
        """Test case verifies that all products associated with a specific category display when the product category is requested"""

        # Guest user, searching for product category 1
        response = self.client.get(reverse('website:product_by_category', args=(1,)))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Check that new_product is the only product that shows in the query
        self.assertIn('<h6 class="mb-1">Test Product</h6>'.encode(), response.content)
        self.assertNotIn('<h6 class="mb-1">Test Product2</h6>'.encode(), response.content)

    def test_product_by_category_logged_in_user(self):
        """Test case verifies that when a user (not the seller) is logged in, all products associated with a specific category display when the product category is requested"""

        # Log In user that is not the seller, check that the products not created by the user do show up
        self.client.login(username="test_user", password="secret")

        # Search for product category 1
        response = self.client.get(reverse('website:product_by_category', args=(1,)))

        # Check that status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure that only the product associated with product category 1 is displayed
        self.assertIn('<h6 class="mb-1">Test Product</h6>'.encode(), response.content)
        self.assertNotIn('<h6 class="mb-1">Test Product2</h6>'.encode(), response.content)

        # Search for product category 2
        response_non_seller = self.client.get(reverse('website:product_by_category', args=(2,)))

        # Check that the status code is 200
        self.assertEqual(response_non_seller.status_code, 200)

        # Make sure that only the product associated with product category 2 is displayed
        self.assertNotIn('<h6 class="mb-1">Test Product</h6>'.encode(), response_non_seller.content)
        self.assertIn('<h6 class="mb-1">Test Product2</h6>'.encode(), response_non_seller.content)

    def test_product_by_category_logged_in_seller(self):
        """Test case verifies that if the seller of a product is logged in, they will not see their products when the product category is requested"""

        # Log In user that is the seller, check that their products to do not show up
        self.client.login(username="test_seller", password="secret")

        # Search for product category 1
        response = self.client.get(reverse('website:product_by_category', args=(1,)))

        # Check that status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure that the returned HTML does not include either product
        self.assertNotIn('<h6 class="mb-1">Test Product</h6>'.encode(), response.content)
        self.assertNotIn('<h6 class="mb-1">Test Product2</h6>'.encode(), response.content)

        # Search for product category 2
        response_seller = self.client.get(reverse('website:product_by_category', args=(2,)))

        # Check that the status code is 200
        self.assertEqual(response_seller.status_code, 200)

        # Ensure that the returned HTML does not include either product
        self.assertNotIn('<h6 class="mb-1">Test Product</h6>'.encode(), response_seller.content)
        self.assertNotIn('<h6 class="mb-1">Test Product2</h6>'.encode(), response_seller.content)
