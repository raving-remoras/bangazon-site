from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from website.models import *
import random

@login_required
def cart(request):
    """Gets user's open order and then displays the order with list of its products. If no order exists, the template suggests that the user visit the shopping page.

    Author: Brendan McCray
    Returns: render - cart.html template

    """

    # Order (get order ID where customer id is current user's customer ID) -> OrderProduct (for product IDs on open order) -> Product (get product data)
    sql = """SELECT *
        FROM website_order
        JOIN website_orderproduct ON website_orderproduct.order_id = website_order.id
        JOIN website_product ON website_product.id = website_orderproduct.product_id
        WHERE customer_id = %s AND website_order.payment_type_id IS NULL
    """

    if request.method == "GET":
        customer_id = request.user.customer.id
        # get user's open order information. If there's no open order, then the context is effectively empty, and logic within the template responds accordingly
        order = Order.objects.raw(sql, [customer_id])

        # get products from queryset to provide the template with a morobvious context variable
        products = list()
        for product in order:
            products.append(product)

        # calculate total cost of products in open order
        total = 0
        for product in order:
            total += product.price

        context = {"order_id": order[0].id, "order": order, "products": products, "total":total}
        return render(request, "cart.html", context)