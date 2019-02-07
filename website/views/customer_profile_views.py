from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User


from website.forms import UserForm, ProductForm
from website.models import Product

@login_required
def customer_profile(request):
    user = request.user
    context = {"user": request.user}
    return render(request, 'customer_profile.html', context)


