from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm
from .models import Product


def all_products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    context = {
        "products": products,
        "current_time": datetime.now(),
    }
    return render(request, "products.html", context)


def registration_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("all_products")
    else:
        form = CustomUserCreationForm()

    context = {
        "form": form,
    }
    return render(request, "registration.html", context)
