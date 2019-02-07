from django.urls import path
from . import views

app_name = "website"
urlpatterns = [

    path("", views.index, name='index'),
    path("login", views.login_user, name='login'),
    path("logout", views.user_logout, name='logout'),
    path("register", views.register, name='register'),
    path("sell", views.sell_product, name='sell'),
    path("list_products", views.list_products, name='list_products'),
    path("customer/add_payment", views.add_ name="add_payment")

]