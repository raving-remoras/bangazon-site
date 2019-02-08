from django.shortcuts import get_object_or_404, render
from website.models import Product, OrderProduct, Order

def list_products(request):
    if not request.user.is_authenticated:
        all_products = Product.objects.raw(f"""
            SELECT * FROM website_product
        """)
    else:
        user_id = request.user.customer.id
        all_products = Product.objects.raw(f"""
            SELECT * FROM website_product
            WHERE website_product.seller_id IS NOT {user_id}
        """)

    template_name = 'product_list.html'
    return render(request, template_name, {'products': all_products})


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


def my_products(request):
    """This method gets customer from user in cookies, renders payment_form.html, and adds a new payment method to the database for the current customer upon submit

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
    purchased_counts = []
    remaining_counts = []
    cart_counts = []
    for product in my_products:
        purchased_count = get_purchased_count(product.id)
        purchased_counts.append(purchased_count)
        remaining_count = product.quantity - purchased_count
        remaining_counts.append(remaining_count)
        cart_count = get_cart_count(product.id)
        cart_counts.append(cart_count)


    return render(request, "my_products.html", {'products': my_products, "purchased_counts": purchased_counts, "cart_counts": cart_counts, "remaining_counts": remaining_counts})

def product_item(request, product):
    purchased_count = get_purchased_count(product.id)
    remaining_count = product.quantity - purchased_count
    cart_count = get_cart_count(product.id)

    return render(request, "product_item.html", {"product": product, "purchased_count": purchased_count})