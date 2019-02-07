from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from website.models import *

@login_required
def cart(request):
    if request.method == "GET":
        user_id = request.user.customer.id

        sql = """SELECT *
        FROM website_order
        WHERE customer_id = %s AND website_order.payment_type_id IS NULL
        """
        order = Order.objects.raw(sql, [user_id])[0]
        items = None

        context = {"order": order, "items": items}
        return render(request, "cart.html", context)
