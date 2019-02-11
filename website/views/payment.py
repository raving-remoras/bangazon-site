from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from website.models import *
from django.db import connection

@login_required(login_url="/website/login")
def payment(request):
    """Gets information about the user's payment types and renders a template with a select dropdown. If user specifies "Done" in template, the POST will close the logged in user's open order in the database.

        Author: Brendan McCray
        Returns:
            1. render - payment.html if loading page
            2. httpRedirect - products view with success message
    """
    customer_id = request.user.customer.id

    # Order (get order ID where customer id is current user's customer ID) -> OrderProduct (for product IDs on open order) -> Product (get product data)
    sql = """SELECT *
        FROM website_order
        JOIN website_orderproduct ON website_orderproduct.order_id = website_order.id
        JOIN website_product ON website_product.id = website_orderproduct.product_id
        WHERE customer_id = %s AND website_order.payment_type_id IS NULL
    """

    # PaymentType (get payment options where the card/account hasn't been deleted)
    sql_payment = """SELECT id, name, substr(account_number, -4, 4) as last_4
        FROM website_paymenttype
        WHERE customer_id = %s AND delete_date IS NULL
    """

    if request.method == "GET":
        # get user's open order information. If there's no open order, then the context is effectively empty, and logic within the template responds accordingly
        order = Order.objects.raw(sql, [customer_id])

        # calculate total cost of products in open order
        total = 0
        for product in order:
            total += product.price

        # query database for all of user's saved - and non-deleted - payment options
        payment_options = PaymentType.objects.raw(sql_payment, [customer_id])

        context = {"order_id": order[0].id, "order": order, "total": total, "payment_options": payment_options}
        return render(request, "payment.html", context)

    if request.method == "POST":
        # Update payment_type_id in Order table to "close" the open order
        payment_id = request.POST["payment_method"]
        sql = "UPDATE website_order SET payment_type_id = %s WHERE customer_id = %s AND payment_type_id IS NULL"
        with connection.cursor() as cursor:
            cursor.execute(sql, [payment_id, customer_id])
        # provide confirmation to user on redirect
        messages.success(request,"Thank you for placing your order!")
        return HttpResponseRedirect(reverse('website:products'))
    else:
        context = {}
        return render(request, "cart.html", context)