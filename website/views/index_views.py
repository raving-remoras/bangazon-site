from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext

from website.forms import ProductForm
from website.models import Product

def index(request):
    template_name = 'index.html'
    return render(request, template_name, {})


def sell_product(request):
    if request.method == 'GET':
        product_form = ProductForm()
        template_name = 'product/create.html'
        return render(request, template_name, {'product_form': product_form})

    elif request.method == 'POST':
        form_data = request.POST

        p = Product(
            seller = request.user,
            title = form_data['title'],
            description = form_data['description'],
            price = form_data['price'],
            quantity = form_data['quantity'],
        )
        p.save()
        template_name = 'product/success.html'
        return render(request, template_name, {})

def list_products(request):
    all_products = Product.objects.all()
    template_name = 'product_list.html'
    return render(request, template_name, {'products': all_products})






