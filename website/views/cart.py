from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from website.models import *
import random

@login_required
def cart(request):
    """Determines the order ID of the user's open order and then displays the order with list of its products. If no order exists, the template suggests that the user visit the shopping page.

    Author: Brendan McCray
    Returns: render - cart.html template

    """

    sql = """SELECT *
        FROM website_order
        WHERE customer_id = %s AND website_order.payment_type_id IS NULL
    """

    sql_2 = """SELECT *
        FROM website_orderproduct
        WHERE order_id = %s
    """

    sql_3 = """SELECT *
        FROM website_product
        WHERE id = %s
    """

    if request.method == "GET":
        user_id = request.user.customer.id
        try:
            # get order ID of user's open order. The try/except Index error is based on the order variable's raw SQL (note: [0]). If there's no open order, there's an index error because there is no index [0] in the list!
            order = Order.objects.raw(sql, [user_id])[0]

            # get IDs of products in the open order
            product_ids = OrderProduct.objects.raw(sql_2, [order.id])

            # get products from product IDs
            products = list()
            for row in product_ids:
                product = Product.objects.raw(sql_3, [row.product_id])[0]
                products.append(product)

            context = {"order": order, "products": products}
        # If there is no order, then pass no context to the cart template
        except IndexError:
            context = {}

        return render(request, "cart.html", context)

#             sql_2 = """SELECT *
#         FROM website_orderproduct
#         WHERE order_id = %s
#     """

#     sql_3 = """SELECT *
#         FROM website_product
#         WHERE id = %s
#     """

#     if request.method == "GET":
#         user_id = request.user.customer.id
#         try:
#             # get order ID of user's open order. The try/except Index error is based on the order variable's raw SQL (note: [0]). If there's no open order, there's an index error because there is no index [0] in the list!
#             order = Order.objects.raw(sql, [user_id])[0]

#             # get IDs of products in the open order
#             product_ids = OrderProduct.objects.raw(sql_2, [order.id])

#             # get products from product IDs
#             products = list()
#             for row in product_ids:
#                 product = Product.objects.raw(sql_3, [row.product_id])[0]
#                 products.append(product)

#             context = {"order": order, "products": products}
#         # If there is no order, then pass no context to the cart template
#         except IndexError:
#             context = {}

#         return render(request, "cart.html", context)