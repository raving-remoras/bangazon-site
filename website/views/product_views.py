import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from django.contrib.auth.decorators import login_required
from website.models import Product, OrderProduct, Order


def list_local_results(request):
    """Process the POST request to list_products to display search results.

        Author: Sebastian Civarolo

        Returns:
            context [dict] -- Contains the data to be passed into the template for search results
    """
    search_data = request.POST

    if "city" in search_data:
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



def list_products(request):
    """ Handles the main product list view.

        Authors: Kelly Morin, Sebastian Civarolo

    """

    if not request.user.is_authenticated:
        if request.method == "POST":
            context = list_local_results(request)

        else:
            all_products = Product.objects.raw(f"""
                SELECT * FROM website_product
            """)
            context = {
                "products": all_products
            }
    else:

        if request.method == "POST":
            context = list_local_results(request)

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



def get_purchased_count(product_id):
    """This method gets all completed orders for a specific product and calculates the number purchased

    Author: Kelly Morin; refactored by Rachel Daniel

    Returns:
        purchased_count
    """
    purchased_qty = OrderProduct.objects.raw(f"""
        SELECT * FROM website_orderproduct
        LEFT JOIN website_order ON website_order.id = website_orderproduct.order_id
        WHERE website_order.payment_type_id IS NOT null
        AND website_orderproduct.product_id = {product_id}
    """)

    purchased_count = 0
    for item in purchased_qty:
        if item.product_id == product_id:
            purchased_count += 1

    return purchased_count

def get_cart_count(product_id):
    """This method gets all incomplete orders for a specific product and calculates the number currently in the carts of all users

    Author: Kelly Morin; refactored by Rachel Daniel

    Returns:
        cart_count
    """

    cart_qty = OrderProduct.objects.raw(f"""
        SELECT * FROM website_orderproduct
        LEFT JOIN website_order ON website_order.id = website_orderproduct.order_id
        WHERE website_order.payment_type_id IS null
        AND website_orderproduct.product_id = {product_id}
    """)

    cart_count = 0
    for item in cart_qty:
        if item.product_id == product_id:
            cart_count +=1

    return cart_count

def product_details(request, product_id):
    product_details = Product.objects.raw(f"""
        SELECT * FROM website_product
        WHERE website_product.id == {product_id}
    """)[0]

    purchased_count = get_purchased_count(product_id)
    cart_count = get_cart_count(product_id)
    available_qty = product_details.quantity - purchased_count

    context = {
        "product_details": product_details,
        "quantity": available_qty,
        "cart_count": cart_count
    }
    return render(request, "product_detail.html", context)

@login_required(login_url="/website/login")
def my_products(request):
    """This method gets customer from user in cookies and renders my_products.html

    Author: Rachel Daniel

    Returns:
        render -- loads the payment_form.html template using the PaymentForm class in forms.py when originally navigating to the page
        HttpResponseRedirect -- TODO: loads the customer profile if add was successful
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


@login_required()
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
