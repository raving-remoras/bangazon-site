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
                    messages.success(request, 'Saved!')
                return HttpResponseRedirect(reverse("website:index"))
