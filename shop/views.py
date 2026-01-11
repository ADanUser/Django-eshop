from django.http import HttpResponse, HttpRequest
from shop.models import Product


def all_products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    html_content = "<h1>Список всех продуктов</h1><ul>"
    for product in products:
        html_content += f"<li>{product.title} — {product.price}</li>"
    html_content += "</ul>"
    return HttpResponse(html_content)

# Create your views here.
