from django.test import TestCase
from ..models import *
from django.urls import reverse

class ClosedOrderTest(TestCase):
    """Tests that a closed order displays correctly on the page.

                Model: Order, Customer, Product, Order_Product, PaymentType

                Template: closed_order.html

                Views: closed_order

                Author: Jase Hackman
    """

    def test_closed_order_render(self):
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