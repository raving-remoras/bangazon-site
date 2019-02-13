from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    # ex. /
    path("", views.index, name='index'),
    # ex. /login
    path("login", views.login_user, name='login'),
    # ex. /logout
    path("logout", views.user_logout, name='logout'),
    # ex. /register
    path("register", views.register, name='register'),
    # ex. /sell
    path("sell", views.sell_product, name='sell'),
    # ex. /customer
    path("customer", views.customer_profile, name='customer_profile'),
    # ex. /order
    path("order", views.closed_order, name="closed_order"),
    # ex. /cart
    path("cart", views.cart, name='cart'),
    # ex. /customer/payment
    path("cart/payment", views.payment, name='payment'),
    # ex. /customer/add_payment
    path("customer/add_payment", views.add_payment, name="add_payment"),
    path("customer/payment/<int:payment_id>/delete", views.delete_payment_type, name="delete_payment_type"),
    # ex. /products
    path("products/", views.list_products, name='products'),
    # ex. /products/5
    path("products/<int:product_id>", views.product_details, name="product_details"),
    # ex. /product-categories
    path("product-categories", views.product_categories, name="product_categories"),
    # ex. /products/5/add
    path("products/<int:product_id>/add", views.add_to_cart, name="add_to_cart"),
    # ex. /my_products
    path("my_products", views.my_products, name="my_products"),
    # ex. /my_products/5
    path("my_products/<int:product_id>", views.delete_product, name="delete_product"),
    path("products/<int:product_id>/recommend", views.recommend_product, name="recommend_product"),
    path("my_recommendations", views.my_recommendations, name="my_recommendations")
]