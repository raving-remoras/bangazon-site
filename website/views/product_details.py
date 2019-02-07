from django.shortcuts import get_object_or_404, render
from website.models import *


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

    count = 0
    for item in purchased_qty:
        if item.product_id == product_id:
            count += 1

    available_qty = product_details.quantity - count

    context = {
        "product_details": product_details,
        "quantity": available_qty
    }
    return render(request, "product_detail.html", context)
