from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext

from website.forms import ProductForm
from website.models import Product, ProductType, RecommendedProduct

def index(request):
    sql = f"""
            SELECT * FROM website_recommendedproduct
            WHERE recommended_to_id = {request.user.customer.id}
    """

    rec_products = RecommendedProduct.objects.raw(sql)
    count = 0
    if rec_products:
        for prod in rec_products:
            count += 1
    print("@@@@@@@@",count)

    product_categories = ProductType.objects.raw(f"""
        SELECT * FROM website_producttype
    """)
    context = {"product_categories": product_categories, "count": count}
    template_name = 'index.html'
    return render(request, template_name, context)
