from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from website.models import *
from django.db import connection

@login_required(login_url="/website/login")
def cart(request):
    """Gets user's open order and then displays the order with list of its products. If no order exists, the template suggests that the user visit the shopping page.

    Author: Brendan McCray
    Returns: render - cart.html template

    """

    customer_id = request.user.customer.id

    sql_delete = """DELETE FROM website_orderproduct
        WHERE order_id = %s AND product_id = %s
    """

    if request.method == "POST":
        product_id = request.POST["product_id"]
        order_id = request.POST["order_id"]
        with connection.cursor() as cursor:
            cursor.execute(sql_delete, [order_id, product_id])
        return HttpResponseRedirect(reverse("website:cart"))

    # Order (get order ID where customer id is current user's customer ID) -> OrderProduct (for product IDs on open order) -> Product (get product data)
    sql = """SELECT *
        FROM website_order
        JOIN website_orderproduct ON website_orderproduct.order_id = website_order.id
        JOIN website_product ON website_product.id = website_orderproduct.product_id
        WHERE customer_id = %s AND website_order.payment_type_id IS NULL
    """

    try:
        if request.method == "GET":
            # get user's open order information. If there's no open order, then the context is effectively empty, and logic within the template responds accordingly. The order table returned (i.e. the order variable) has one row per product
            order = Order.objects.raw(sql, [customer_id])

            # get products from queryset (effectively the same rows as the order variable already has) to provide the template with a more obvious context variable
            products = list()
            for product in order:
                products.append(product)

            # calculate total cost of products in open order
            total = 0
            for product in order:
                total += product.price

            context = {"order_id": order[0].id, "order": order, "products": products, "total": total}
            return render(request, "cart.html", context)
    except:
        context = {}
        return render(request, "cart.html", context)