from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext

from website.forms import ProductForm
from website.models import Product

def list_products(request):
    all_products = Product.objects.all()
    template_name = 'product_list.html'
    return render(request, template_name, {'products': all_products})