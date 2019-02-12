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
        render -- loads the recommend_product.html template using the PaymentForm class in forms.py when originally navigating to the page
        HttpResponseRedirect -- sends the user back to login if not authenticated, back to the same form page if entered user is not in the database, and back to the detail page they came from if post is successful
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


def my_recommendations(request):
    if request.method == "GET":
        sql = f"""
            SELECT P.*, R.*, C.id as from_cust_id, U.username as from_username FROM website_product P
            JOIN website_recommendedproduct R on R.product_id = P.id
            JOIN website_customer C on C.id = R.recommended_by_id
            JOIN auth_user U on U.id = C.user_id
            WHERE R.recommended_to_id = {request.user.customer.id}
    """

        products = Product.objects.raw(sql)
        return render(request, "my_recommendations.html", {"products": products})




