import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from website.models import *
from website.forms import *


@login_required(login_url="/website/login")
def add_payment(request):
    """This method gets customer from user in cookies, renders payment_form.html, and adds a new payment method to the database for the current customer upon submit

    Author: Rachel Daniel

    Returns:
        render -- loads the payment_form.html template using the PaymentForm class in forms.py when originally navigating to the page
        HttpResponseRedirect -- TODO: loads the customer profile if add was successful
    """

    customer = request.user.customer

    if request.method == "GET":
        form = PaymentForm()
        context = {"customer":customer, "form":form}
        return render(request, "payment_form.html", context)

    if request.method == "POST":
            form = PaymentForm(request.POST)
            if form.is_valid():
                cleaned = form.cleaned_data
                name = cleaned["name"]
                account_number = cleaned["account_number"]
                sql = "INSERT into website_paymenttype (name, account_number, customer_id) VALUES (%s, %s, %s)"

                with connection.cursor() as cursor:
                    cursor.execute(sql, [name, account_number, customer.id])
                    # messages.success(request, 'Saved!')
                return HttpResponseRedirect(reverse("website:customer_profile"))


@login_required(login_url="/website/login")
def delete_payment_type(request, payment_id):
    """Delete a payment type if it is the current user's.

        Author: Sebastian Civarolo

        Params:
            payment_id [int] - ID to query

        Returns:
            If payment_type.customer_id matches current user, confirmation page
            If payment_type.customer_id does not match current user, redirect to user settings
    """

    if request.method == "GET":

        customer_id = request.user.customer.id

        # Get the payment type from the Database
        payment_type = PaymentType.objects.raw('''
            SELECT * FROM website_paymenttype
            WHERE id = %s
        ''', [payment_id])

        if request.user.customer.id == payment_type[0].customer_id:
            # Load the confirmation page if current user owns this payment type
            context = {
                "payment_type": payment_type[0]
            }
            return render(request, "payment_delete.html", context)
        else:
            # If someone tries to manually go to delete a payment type url that is not theirs, redirect them.
            return HttpResponseRedirect(reverse("website:customer_profile"))


    elif request.method == "POST":

        orders_sql = """
            SELECT * FROM website_order
            WHERE website_order.payment_type_id == %s
        """

        orders_with_payment = Order.objects.raw(orders_sql, [payment_id])

        if len(orders_with_payment):
            # Soft delete if this payment type has been used to complete an order.
            sql_soft_delete = """
                UPDATE website_paymenttype
                SET delete_date = %s
                WHERE id = %s
            """
            values = [datetime.datetime.now(), payment_id]
            with connection.cursor() as cursor:
                cursor.execute(sql_soft_delete, values)

        else:
            # If this payment type has never been used, hard delete.
            sql_delete = """
                DELETE FROM website_paymenttype
                WHERE id = %s
            """
            values = [payment_id]
            with connection.cursor() as cursor:
                cursor.execute(sql_delete, values)

        return HttpResponseRedirect(reverse("website:customer_profile"))
