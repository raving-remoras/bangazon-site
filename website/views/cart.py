from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from website.models import *
from django.db import connection

@login_required(login_url="/website/login")
def cart(request):
    """1. Gets user's open order and then displays the order with list of its products. If no order exists, the template suggests that the user visit the shopping page.
    2. Handles deletion of products from the user's cart using a nested if--try/except--try/except. Comments included in file

    Author: Brendan McCray
    Returns:
        1. HttpResponseRedirect - when an order is deleted in its entirety, the user is redirected to the products page (product_list.html)
        1. HttpResponseRedirect - when a product is deleted from the cart (cart.html), user is returned to their cart (i.e. cart instantly updates)
        2. render - displays user's cart when 'cart' is clicked in the navbar (cart.html)
    """

    # ---------------------------------------------------------------
    # Used to load user's cart
    # Order (get order ID where customer id is current user's customer ID) -> OrderProduct (for product IDs on open order) -> Product (get product data)
    sql = """SELECT *, website_orderproduct.id as "order_product_id"
        FROM website_order
        JOIN website_orderproduct ON website_orderproduct.order_id = website_order.id
        JOIN website_product ON website_product.id = website_orderproduct.product_id
        WHERE customer_id = %s AND website_order.payment_type_id IS NULL
    """

    # used to delete single join table
    sql_delete = """DELETE FROM website_orderproduct
        WHERE order_id = %s AND id = %s
    """

    # used to delete the user's open order
    sql_delete_open_order = """DELETE FROM website_order
        WHERE website_order.id = %s AND website_order.payment_type_id IS NULL
    """
    # ---------------------------------------------------------------

    customer_id = request.user.customer.id

    # A delete button was clicked - if it's the 'cancel order' button AND!!! the user provides confirmation, then delete all OrderProduct join tables and the open order. Otherwise, delete the specific product that was clicked.
    if request.method == "POST":

        try:
            cancel_order_confirmation = request.POST["confirmed_deletion"] # if this is exists on POST, then the user has confirmed the order's deletion. if not -> except
            order_id = request.POST["order_id"]
            products = Order.objects.raw(sql, [customer_id])

            for product in products:
                with connection.cursor() as cursor:
                    cursor.execute(sql_delete, [order_id, product.order_product_id])

            with connection.cursor() as cursor:
                cursor.execute(sql_delete_open_order, [order_id])

            return HttpResponseRedirect(reverse("website:products"))

        except:

            try:
                cancel_order = request.POST["empty_cart"] # if this exists on POST, then the user clicked the cancel all button, so prompt for confirmation. if not -> except
                context = {"order_id": request.POST["order_id"], "delete_confirmation": True}
                return render(request, "cart.html", context)

            except:
                # last valid option that would trigger a POST: a user clicked delete button on a specific product in their cart, so remove it
                order_product_id = request.POST["order_product_id"]
                order_id = request.POST["order_id"]
                with connection.cursor() as cursor:
                    cursor.execute(sql_delete, [order_id, order_product_id])

                # check if there are remaining items in cart. If cart is empty, delete open order
                order = Order.objects.raw(sql, [customer_id])
                order_size = len(order)
                if order_size == 0:
                    with connection.cursor() as cursor:
                        cursor.execute(sql_delete_open_order, [order_id])

                # redirect user back to their cart
                return HttpResponseRedirect(reverse("website:cart"))

    # load user's cart when clicking the link in the navbar.
    try:
        if request.method == "GET":
            # get user's open order information. If there's no open order, then the context is effectively empty, and the except clause takes effect. If an order table is returned (i.e. the order variable), then it has one row per product
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