from django.shortcuts import get_object_or_404, render
from website.models import Product, OrderProduct, Order

def list_products(request):
    all_products = Product.objects.all()
    template_name = 'product_list.html'
    return render(request, template_name, {'products': all_products})

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
