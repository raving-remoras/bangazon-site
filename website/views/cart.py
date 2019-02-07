from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from website.models import *

@login_required
def view_open_order(request):
    if request.method == "GET":
        user_id = request.user.id
        sql = """SELECT *
        FROM website_order
        WHERE auth_user = %s AND website_order.payment_type_id IS NOT NULL
        """
        order = Order.objects.raw(sql, [user_id])[0]

        context = {"order": order}
        return render(request, 'cart.html', context)

# def add_brand(request):
#     '''View for adding bike brands
#     Allowed verbs: GET, POST
#     returns form to post new bike brands and redirects users to a link to list of bike brands
#     '''
#     if request.method == "GET":
#         #render the form page
#         brand_form = BrandForm()
#         return render(request, 'brands/create.html', {"brand_form": brand_form})

#     if request.method == "POST":
#         form_data = request.POST

#         newBrand = Brand(
#             name = form_data['name'],
#             location = form_data['location'],
#         )
#         newBrand.save()
#         messages.success(request, 'Saved!')
#         return HttpResponseRedirect(reverse("bikes:brand_list"))
