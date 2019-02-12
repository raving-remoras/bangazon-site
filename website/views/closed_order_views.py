from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from website.forms import *
from django.db import connection


@login_required
def closed_order(request):
    """Renders a page using an order id to display a closed order.

        Model: Order, Product, Order_Product, PaymentType

        Template: closed_order.html

        Author: Jase Hackman
    """
    if "rating" in request.POST:
        save_product_rating(request)

    order_id = request.POST["order_id"]
    order = Order.objects.raw("Select * From website_order WHERE id=%s", [order_id])
    order_products = OrderProduct.objects.raw("Select * FROM website_orderproduct op Join website_product p on op.product_id=p.id WHERE order_id=%s", [order_id])
    total = 0
    for product in order_products:
        total += product.price

    context = {
        "order": order[0],
        "order_products": order_products,
        "total": total
    }

    return render(request, 'closed_order.html', context)


def save_product_rating(request):
    """ Called in closed_order to save the user's product rating to the database.

        Author: Sebastian Civarolo
    """
    data = request.POST
    rating = data['rating']
    orderproduct = data['orderproduct_id']
    params = [rating, orderproduct]
    sql = """
        UPDATE website_orderproduct
        SET rating = %s
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, params)

