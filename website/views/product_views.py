from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import connection
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from website.models import Product, OrderProduct, Order

def list_products(request):
    if not request.user.is_authenticated:
        all_products = Product.objects.raw(f"""
            SELECT * FROM website_product
        """)
        context = {
            "products": all_products
        }

    else:
        user_id = request.user.customer.id
        all_products = Product.objects.raw(f"""
            SELECT * FROM website_product
            WHERE website_product.seller_id IS NOT {user_id}
        """)
        context = {
            "products": all_products
        }

    template_name = 'product_list.html'
    return render(request, template_name, context)

def product_details(request, product_id):
    product_details = Product.objects.raw(f"""
        SELECT * FROM website_product
        WHERE website_product.id == {product_id}
    """)[0]

    purchased_qty = OrderProduct.objects.raw(f"""
        SELECT * FROM website_orderproduct
        LEFT JOIN website_order ON website_order.id = website_orderproduct.order_id
        WHERE website_order.payment_type_id IS NOT null
        AND website_orderproduct.product_id = {product_id}
    """)

    cart_qty = OrderProduct.objects.raw(f"""
        SELECT * FROM website_orderproduct
        LEFT JOIN website_order ON website_order.id = website_orderproduct.order_id
        WHERE website_order.payment_type_id IS null
        AND website_orderproduct.product_id = {product_id}
    """)

    purchased_count = 0
    for item in purchased_qty:
        if item.product_id == product_id:
            purchased_count += 1

    cart_count = 0
    for item in cart_qty:
        if item.product_id == product_id:
            cart_count +=1

    available_qty = product_details.quantity - purchased_count

    context = {
        "product_details": product_details,
        "quantity": available_qty,
        "cart_count": cart_count
    }
    return render(request, "product_detail.html", context)

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        product_details = Product.objects.raw(f"""
            SELECT * FROM website_product
            WHERE website_product.id == {product_id}
        """)[0]

        purchased_qty = OrderProduct.objects.raw(f"""
            SELECT * FROM website_orderproduct
            LEFT JOIN website_order ON website_order.id = website_orderproduct.order_id
            WHERE website_order.payment_type_id IS NOT null
            AND website_orderproduct.product_id = {product_id}
        """)

        cart_qty = OrderProduct.objects.raw(f"""
            SELECT * FROM website_orderproduct
            LEFT JOIN website_order ON website_order.id = website_orderproduct.order_id
            WHERE website_order.payment_type_id IS null
            AND website_orderproduct.product_id = {product_id}
        """)

        purchased_count = 0
        for item in purchased_qty:
            if item.product_id == product_id:
                purchased_count += 1

        cart_count = 0
        for item in cart_qty:
            if item.product_id == product_id:
                cart_count +=1

        available_qty = product_details.quantity - purchased_count

        context = {
            "product_details": product_details,
            "quantity": available_qty,
            "cart_count": cart_count,
            "error_message": "Please login to continue"
        }
        return render(request, "product_detail.html", context)
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

            return HttpResponseRedirect(reverse('website:products'))
            # TODO: Need to figure out how to add success message
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
            return HttpResponseRedirect(reverse('website:products'))
