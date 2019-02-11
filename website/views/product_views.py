from django.shortcuts import get_object_or_404, render
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
