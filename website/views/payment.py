from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from website.models import *

@login_required
def payment(request, order_id):
    # Attempting to access the payment selection page when there is no open order redirects the user to the empty card message
    if request.method == "GET":
        context = {}
        return render(request, "cart.html", context)
    elif request.method == "POST":
        context = {"order": order, "total": total}
        return render(request, "cart.html", context)
    else:
        context = {}
        return render(request, "cart.html", context)