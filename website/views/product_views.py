from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import connection
from django.urls import reverse
import datetime
from django.shortcuts import get_object_or_404, render
from website.models import Product, OrderProduct, Order


def list_products(request):
    """ Handles the main product list view.

        Authors: Kelly Morin, Sebastian Civarolo

    """
    if not request.user.is_authenticated:
        if request.method == "POST":
            context = list_search_results(request)

        else:
            all_products = Product.objects.raw(f"""
                SELECT * FROM website_product
            """)
            context = {
                "products": all_products
            }
    else:

        if request.method == "POST":
            context = list_search_results(request)

        elif request.method == "GET":

            user_id = request.user.customer.id
            all_products = Product.objects.raw(f"""
                SELECT * FROM website_product
                WHERE website_product.seller_id IS NOT {user_id}
            """)

            context = {
                "products": all_products
            }

    template_name = "product_list.html"
    return render(request, template_name, context)


def list_search_results(request):
    """Process the POST request to list_products to display search results.

        Author: Sebastian Civarolo

        Returns:
            context [dict] -- Contains the data to be passed into the template for search results
    """
    search_data = request.POST

    if "product_query" in search_data:
        product_query = "%" + search_data["product_query"] + "%"

        if request.user.is_authenticated:
            seller_id = request.user.customer.id
            sql = """
                SELECT * FROM website_product
                WHERE website_product.seller_id IS NOT %s
                AND website_product.title LIKE %s
                AND website_product.delete_date IS NULL
            """
            params = [seller_id, product_query]

        else:
            sql = """
                SELECT * FROM website_product
                WHERE website_product.title LIKE %s
                AND website_product.delete_date IS NULL
            """
            params = [product_query]

        search_results = Product.objects.raw(sql, params)
        search_query = search_data["product_query"]

        context = {
            "products": search_results,
            "product_query": search_query
        }


    elif "city" in search_data:
        city = "%" + search_data["city"] + "%"

        if request.user.is_authenticated:
            sql = """
                SELECT * FROM website_product
                WHERE website_product.seller_id IS NOT %s
                AND website_product.local_delivery IS 1
                AND website_product.delivery_city LIKE %s
            """
            seller_id = request.user.customer.id
            local_products = Product.objects.raw(sql, [seller_id, city])

        else:
            sql = """
                SELECT * FROM website_product
                WHERE website_product.delivery_city LIKE %s
                AND website_product.local_delivery IS 1
            """
            local_products = Product.objects.raw(sql, [city])


        context = {
            "products": local_products,
            "city_query": search_data["city"]
        }

    return context


def product_details(request, product_id):
    # TODO: Update cart feature so it only shows the number of people that have an item in their cart if the user is not the active user
    product_details = Product.objects.raw(f"""
        SELECT * FROM website_product
        JOIN auth_user ON auth_user.id == website_product.seller_id
        WHERE website_product.id == {product_id}
    """)[0]

    context = {
        "product_details": product_details
    }
    return render(request, "product_detail.html", context)


def add_to_cart(request, product_id):
    """Allows logged in user to add an item to their cart. If they do not have an existing order, this will create the order for them and then add the item to their cart.

    Author: Kelly Morin

    Returns:
        render -- renders the product_list.html template
    """
    # TODO: Set up redirect to login page if user is not currently logged in, with next parameter passed through to login page so the user is automatically redirected to the product detail page they were previously on
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to continue")
        return HttpResponseRedirect(reverse('website:login'))
    else:
        try:
            open_order = Order.objects.raw(f"""
                SELECT * FROM website_order
                WHERE website_order.customer_id == {request.user.customer.id}
                AND website_order.payment_type_id IS null
            """)[0]
            order_id = open_order.id
            product_id = product_id
            data = [order_id, product_id]
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO website_orderproduct
                    (
                        order_id,
                        product_id
                    )
                    VALUES(
                        %s, %s
                    )
                """, data)

            messages.success(request,"This product has been added to your cart!")
            return HttpResponseRedirect(reverse('website:products'))
        except:
            customer = request.user.customer.id
            data = [customer]
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO website_order
                    (
                        customer_id
                    )
                    VALUES(
                        %s
                    )
                """, data)
                new_order = cursor.lastrowid
                product_id = product_id
                relationship_data = [new_order, product_id]
                cursor.execute("""
                    INSERT INTO website_orderproduct
                    (
                        order_id,
                        product_id
                    )
                    VALUES(
                        %s, %s
                    )
                """, relationship_data)

            messages.success(request,"This product has been added to your cart!")
            return HttpResponseRedirect(reverse('website:products'))


@login_required(login_url="/website/login")
def my_products(request):
    """This method gets customer from user in cookies and renders my_products.html

    Author: Rachel Daniel

    Returns:
        render -- loads the payment_form.html template using the PaymentForm class in forms.py when originally navigating to the page
    """
    customer = request.user.customer
    sql = """
            SELECT * FROM website_product P
            JOIN website_producttype PT ON PT.id = P.product_type_id
            WHERE P.seller_id = %s
			AND P.delete_date is null
        """

    my_products = Product.objects.raw(sql, [customer.id])

    return render(request, "my_products.html", {'products': my_products})


@login_required(login_url="/website/login")
def delete_product(request, product_id):
    """This method gets product from the id passed into the url and renders the delete_product.html template

    Author: Rachel Daniel

    Returns:
        render -- loads delete_product.html template for GET request
        HttpResponseRedirect -- after successful POST, redirects to my_products.html
    """
    sql = """
            SELECT * FROM website_product
            WHERE id = %s
        """
    product = Product.objects.raw(sql, [product_id])
    if request.method == "GET":
        #protect against users typing ids into url for products on which they are not sellers
        if request.user.customer.id == product[0].seller_id:
            return render(request, "delete_product.html", {'product_id': product_id, "product": product[0]})
        else:
            return render(request, "delete_product.html", {"invalid": "invalid"})

    if request.method == "POST":
        now = datetime.datetime.now()
        update_prod_sql = """
            UPDATE website_product SET delete_date = %s WHERE id = %s
        """
        delete_joins_sql = """
            DELETE FROM website_orderproduct WHERE product_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(update_prod_sql, [now, product_id])
        with connection.cursor() as cursor:
            cursor.execute(delete_joins_sql, [product_id])
        return HttpResponseRedirect(reverse("website:my_products"))
