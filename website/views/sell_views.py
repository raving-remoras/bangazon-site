from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.db import connection

from website.forms import ProductForm
from website.models import *

def sell_product(request):
    """Loads the view for creating a product to sell and saves it to the database.

        Author: Sebastian Civarolo

    """
    if request.method == 'GET':
        product_form = ProductForm()
        template_name = 'product/create.html'
        context = {
            'product_form': product_form
        }
        return render(request, template_name, context)

    elif request.method == 'POST':
        form_data = request.POST
        product_form = ProductForm(form_data)

        if product_form.is_valid():

            seller = request.user.customer.id
            title = form_data['title']
            description = form_data['description']
            product_type = form_data['product_type']
            price = form_data['price']
            quantity = form_data['quantity']

            data = [
                seller, title, description, product_type, price, quantity
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
                        quantity
                    )
                    VALUES(
                        %s, %s, %s, %s, %s, %s
                    )
                """, data)
                new_product = cursor.lastrowid


            template_name = 'product/success.html'
            context = {
                "title": title,
                "product_id": new_product
            }
            return render(request, template_name, context)