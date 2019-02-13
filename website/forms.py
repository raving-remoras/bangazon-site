from django.contrib.auth.models import User
from django import forms
from website.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name",)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ("title", "description", "product_type", "price", "quantity", "local_delivery", "delivery_city", "delivery_state")


class UserCustomerFormA(forms.ModelForm):

    class Meta:
        model = User
        fields = ("last_name",)


class UserCustomerFormB(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("phone_number", "street_address", "city", "state", "zipcode", )


class PaymentForm(forms.ModelForm):

    class Meta:
        model = PaymentType
        fields = ("name", "account_number")
        labels = {"name": ("Payment Type Name")}