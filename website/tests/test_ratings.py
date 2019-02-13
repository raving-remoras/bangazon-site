import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, Order, OrderProduct, PaymentType

class TestRatingSystem(TestCase):
    """ Tests adding ratings and displaying ratings around the site.

        Author: Sebastian Civarolo

    """

    def test_add_rating(self):

        # Tests that a closed order displays properly on the page
        new_user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="secret"
        )

        self.client.login(username="testuser", password="secret")

        customer = Customer.objects.create(
            street_address="123 Test LN",
            city="Testas",
            state="TS",
            zipcode="11111",
            phone_number="1111111111",
            user=new_user
        )

        product_type = ProductType.objects.create(
            name="Test Type"
        )

        product = Product.objects.create(
            seller=customer,
            product_type=product_type,
            title="Test Product",
            description="Not a real product",
            price=10,
            quantity=1,
            delete_date=None
        )

        payment = PaymentType.objects.create(
            name="$",
            account_number=123456765432,
            customer_id=1
        )

        order = Order.objects.create(
            customer=customer,
            payment_type=payment
        )

        OrderProduct.objects.create(
            order=order,
            product=product
        )

        self.client.login(username="testuser", password="secret")

        # test submitting a new rating from order page
        response = self.client.post(reverse("website:closed_order"), {"order_id": 1, "rating": 4, "orderproduct_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="rating-4-1" name="rating" checked>'.encode(), response.content)

        # test the rating showing on seller's my products view
        seller_view_response = self.client.get(reverse("website:my_products"))
        self.assertIn('<span class="badge badge-warning">Avg Rating: 4.0 / 5 from 1 customers</span>'.encode(), seller_view_response.content)

        # test the rating showing up on product detail view
        product_detail_response = self.client.get(reverse("website:product_details", args=(1,)))
        self.assertIn('<span class="badge badge-success">Avg Rating: 4.0 / 5 from 1 customers</span>'.encode(), product_detail_response.content)
