from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from shop.models import Product
from datetime import datetime


def all_products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    context = {
        'products': products,
        'current_time': datetime.now(),
    }
    return render(request, 'products.html', context)