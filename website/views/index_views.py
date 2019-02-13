from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext

from website.forms import ProductForm
from website.models import Product, ProductType, RecommendedProduct

def index(request):
    context={}
    template_name = 'index.html'
    return render(request, template_name, context)
