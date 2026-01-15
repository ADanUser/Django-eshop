from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView



from shop.forms import CustomUserCreationForm, UserAuthForm
from shop.models import Product

class AllProductsView(ListView):
    model = Product
    template_name = "products.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_time"] = datetime.now()
        return context



# def all_products(request: HttpRequest) -> HttpResponse:
#     products = Product.objects.all()
#     context = {
#         "products": products,
#         "current_time": datetime.now(),
#     }
#     return render(request, "products.html", context)


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


# def registration_view(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("all_products")
#     else:
#         form = CustomUserCreationForm()

#     context = {
#         "form": form,
#     }
#     return render(request, "registration.html", context)


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


# def login_page(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = UserAuthForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("all_products")
#             else:
#                 messages.error(request, "Неверное имя пользователя или пароль.")
#         else:
#             for error_list in form.errors.values():
#                 for error in error_list:
#                     messages.error(request, error)
    
#     form = UserAuthForm()
        
#     context = {
#         "form": form,
#     }
#     return render(request, "login.html", context)


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("all_products")


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"