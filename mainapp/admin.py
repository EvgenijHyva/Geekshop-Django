from django.contrib import admin
from mainapp.models import ProductCategory, Product


admin.site.register(ProductCategory)
# admin.site.register(Product) для отображения используется метод str


@admin.register(Product)   # регистрируем модель по новой
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity")  # указываем поля для отображения
    fields = ("name", "image", "description", "short_description", ("price", "quantity"), "category")  # соеденение
    # полей
    readonly_fields = ("short_description", ) # поля для чтения
    ordering = ("-name", )  # сортировка по: названию (default: ID) дефис "-" обратный порядок

    search_fields = ("name", "category__name")