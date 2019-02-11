from django.urls import path
from . import views

app_name = "website"
urlpatterns = [

    path("", views.index, name='index'),
    path("login", views.login_user, name='login'),
    path("logout", views.user_logout, name='logout'),
    path("register", views.register, name='register'),
    path("sell", views.sell_product, name='sell'),
    path("customer", views.customer_profile, name='customer_profile'),
    path("order", views.closed_order, name="closed_order"),
    path("cart", views.cart, name='cart'),
    path("cart/payment", views.payment, name='payment'),
    path("customer/add_payment", views.add_payment, name="add_payment"),
    # ex. /website/products
    path("products/", views.list_products, name='products'),
    # ex. /website/products/5
    path("products/<int:product_id>", views.product_details, name="product_details"),
    path("my_products", views.my_products, name="my_products"),
    path("my_products/<int:product_id>", views.delete_product, name="delete_product"),
]