from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.db import connection
from django.urls import reverse

from website.forms import ProductForm
from website.models import *

@login_required(login_url="/website/login")
def sell_product(request):
    """Loads the view for creating a product to sell and saves it to the database.

        Author: Sebastian Civarolo

    """
    if request.method == "GET":
        product_form = ProductForm()
        template_name = "product/create.html"
        context = {
            "product_form": product_form
        }
        return render(request, template_name, context)

    elif request.method == "POST":
        form_data = request.POST
        product_form = ProductForm(form_data)

        if product_form.is_valid():

            seller = request.user.customer.id
            title = form_data["title"]
            description = form_data["description"]
            product_type = form_data["product_type"]
            price = form_data["price"]
            quantity = form_data["quantity"]
            if "local_delivery" in form_data:
                local_delivery = 1
                delivery_city = form_data["delivery_city"]
                delivery_state = form_data["delivery_state"]
            else:
                local_delivery = 0
                delivery_city = ""
                delivery_state = ""

            data = [
                seller, title, description, product_type, price, quantity, local_delivery, delivery_city, delivery_state
            ]

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO website_product
                    (
                        seller_id,
                        title,
                        description,
                        product_type_id,
                        price,
                        quantity,
                        local_delivery,
                        delivery_city,
                        delivery_state
                    )
                    VALUES(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, data)
                new_product = cursor.lastrowid

            context = {
                "title": title,
                "product_id": new_product
            }

            return HttpResponseRedirect(reverse("website:product_details", args=(new_product,)))