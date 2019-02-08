from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from website.models import *
from django.db.models.fields import BLANK_CHOICE_DASH


@login_required
def payment(request):

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
        customer_id = request.user.customer.id
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
        context = {}
        return render(request, "cart.html", context)
    else:
        context = {}
        return render(request, "cart.html", context)