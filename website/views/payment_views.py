import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from website.models import *
from website.forms import *


@login_required
def add_payment(request):
    """This method queries the database for the departments and renders the form for adding a new employee. Upon submit, the method collects form data from post request, validates, and adds a new employee

    Author: Rachel Daniel

    Returns:
        render -- loads the employee_form.html template with add context when originally navigating to the page, or renders form with error message if submit was unsuccessful
        HttpResponseRedirect -- loads the employee page if add was successful
    """

    if request.method == "GET":
        customer = request.user
        form = PaymentForm()
        context = {"customer":customer, "form":form}
        return render(request, "payment_form.html", context)