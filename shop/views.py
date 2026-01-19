import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from shop.mixins import IsAuthenticatedMixin
from shop.forms import CustomUserCreationForm, UserAuthForm
from shop.models import Product


class AllProductsView(IsAuthenticatedMixin, ListView):
    model = Product
    template_name = "products.html"
    context_object_name = "products"


class RegistrationView(View):

    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        form = CustomUserCreationForm()
        context = {
            "form": form,
        }
        return render(request, "registration.html", context)

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("all_products")
        context = {
            "form": form,
        }
        return render(request, "registration.html", context)


class LoginView(View):

    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        form = UserAuthForm()
        context = {
            "form": form,
        }
        return render(request, "login.html", context)

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        form = UserAuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("all_products")
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            for error_list in form.errors.values():
                for error in error_list:
                    messages.error(request, error)

        form = UserAuthForm()
        context = {
            "form": form,
        }
        return render(request, "login.html", context)


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("all_products")


@method_decorator(ensure_csrf_cookie, name="dispatch")
class ProductDetailView(IsAuthenticatedMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class CartView(View):

    @staticmethod
    def get(request: HttpRequest, product_id: int) -> HttpResponse:
        cart = request.session.get("cart")

        if cart is None:
            return JsonResponse({ "detail": "Cart does not exist" }, status=404)

        if str(product_id) not in cart:
            return JsonResponse({ "detail": "Product not in cart" }, status=404)
        
        return JsonResponse({"quantity": cart[str(product_id)]}, status=200)


    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        
        data = json.loads(request.body.decode("utf-8"))

        product_id = data["productId"]
        quantity = data["quantity"]

        cart = request.session.get("cart")

        if cart is None:
            cart = {}

        if str(product_id) not in cart:
            cart[str(product_id)] = quantity
        else:
            cart[str(product_id)] += quantity

        request.session.update({"cart": cart})

        return JsonResponse({"success": True})


    @staticmethod
    def delete(request: HttpRequest, product_id: int) -> HttpResponse:

        cart = request.session.get("cart")

        if cart is None:
            return JsonResponse({ "detail": "Cart does not exist" }, status=404)

        if str(product_id) not in cart:
            return JsonResponse({ "detail": "Product not in cart" }, status=404)

        del cart[str(product_id)]
        request.session.update({"cart": cart})
        return JsonResponse({},status=204)