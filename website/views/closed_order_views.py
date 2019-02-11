from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from website.forms import *
from django.db import connection


@login_required(login_url="/website/login")
def closed_order(request):
    order_id = request.POST["order_id"]
    order = Order.objects.raw("Select * From website_order WHERE id=%s", [order_id])
    order_products = OrderProduct.objects.raw("Select * FROM website_orderproduct op Join website_product p on op.product_id=p.id WHERE order_id=%s", [order_id])
    total=0
    for product in order_products:
        total += product.price
    context = {
        "order": order[0],
        "order_products": order_products,
        "total": total
    }

    return render(request, 'closed_order.html', context)


