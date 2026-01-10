from django.contrib import admin
from shop.models import Product, ProductImage, Attribute
from shop.filters import StockFilter

# @admin.action(description="Сбросить остатки до 0")
# def reset_stock(model_admin, request, queryset):
#     updated_count = queryset.update(stock=0)
#     model_admin.message_user(request, f"Остатки сброшены у {updated_count} товаров.")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'images', 'get_attributes')
    list_filter = (StockFilter,)
    search_fields = ('title', 'description')
    actions = ("reset_stock",)    

    @admin.action(description="Сбросить остатки до 0")
    def reset_stock(self, request, queryset):
        updated_count = queryset.update(stock=0)
        self.message_user(request, f"Остатки сброшены у {updated_count} товаров.")

    @admin.display(description='Изображение')
    def images(self, obj: Product):
        return list(obj.productimage_set.values_list('image', flat=True))

    @admin.display(description='Свойства')
    def get_attributes(self, obj: Product):
        return list(obj.attributes.all())

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('productimage_set')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'product')

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
