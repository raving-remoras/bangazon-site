from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from website.models import *
from website.forms import *

def recommend_product(request, product_id):
    """This method gets product information from url and renders recommend_product.html if the request is a GET. When the form is submitted, a new recommendation is inserted into the db

    Author: Rachel Daniel

    Returns:
        render -- loads the payment_form.html template using the PaymentForm class in forms.py when originally navigating to the page
        HttpResponseRedirect -- TODO: loads the customer profile if add was successful
    """

    if not request.user.is_authenticated:
        messages.error(request, "Please log in to continue")
        return HttpResponseRedirect(reverse('website:login'))
    else:
        product = Product.objects.raw('''
            SELECT * FROM website_product
            WHERE id = %s
        ''', [product_id])[0]
        if request.method == "GET":
            return render(request, 'recommend_product.html', {"product": product})

        if request.method == "POST":

            comment = request.POST["comment"]
            recommended_by_id = request.user.customer.id

            user_sql = """
                SELECT u.id, u.username, c.id as 'customer_id' from auth_user u
                JOIN website_customer c on u.id = c.user_id
                WHERE u.username = %s
            """
            recommendee_name =request.POST["recommended_to"]
            recommended_to = User.objects.raw(user_sql, [recommendee_name])

            if recommended_to:
                recommended_to_id = recommended_to[0].customer_id

                insert_sql= "INSERT into website_recommendedproduct (comment, product_id, recommended_by_id, recommended_to_id) VALUES (%s, %s, %s, %s)"
                with connection.cursor() as cursor:
                    cursor.execute(insert_sql, [comment, product_id, recommended_by_id, recommended_to_id])

                messages.success(request, f"Recommended this to {recommendee_name}!")

                return HttpResponseRedirect(reverse("website:product_details", args=(product_id, )))

            else:
                messages.warning(request, f"Oops, couldn't locate a user named {recommendee_name}")

                return HttpResponseRedirect(reverse("website:recommend_product", args=(product_id, )))




