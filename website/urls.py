from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    # ex. /website
    path("", views.index, name='index'),
    # ex. /website/login
    path("login", views.login_user, name='login'),
    # ex. /website/logout
    path("logout", views.user_logout, name='logout'),
    # ex. /website/register
    path("register", views.register, name='register'),
    # ex. /website/sell
    path("sell", views.sell_product, name='sell'),
    # ex. /website/customer
    path("customer", views.customer_profile, name='customer_profile'),
    # ex. /website/order
    path("order", views.closed_order, name="closed_order"),
    # ex. /website/cart
    path("cart", views.cart, name='cart'),
    # ex. /website/customer/payment
    path("cart/payment", views.payment, name='payment'),
    # ex. /website/customer/add_payment
    path("customer/add_payment", views.add_payment, name="add_payment"),
    path("customer/payment/<int:payment_id>/delete", views.delete_payment_type, name="delete_payment_type"),
    # ex. /website/products
    path("products/", views.list_products, name='products'),
    # ex. /website/products/5
    path("products/<int:product_id>", views.product_details, name="product_details"),
    # ex. /website/product-categories
    path("product-categories", views.product_categories, name="product_categories"),
    # ex. /website/products/5/add
    path("products/<int:product_id>/add", views.add_to_cart, name="add_to_cart"),
    # ex. /website/my_products
    path("my_products", views.my_products, name="my_products"),
    # ex. /website/my_products/5
    path("my_products/<int:product_id>", views.delete_product, name="delete_product"),
    path("products/<int:product_id>/recommend", views.recommend_product, name="recommend_product"),
    path("my_recommendations", views.my_recommendations, name="my_recommendations")
]