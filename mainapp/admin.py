from django.contrib import admin
from mainapp.models import ProductCategory, Product


@admin.register(ProductCategory)
class AdminCategory(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", )
    ordering = ("name", "id",)
    search_fields = ("name", )
    list_display = ("id", "name", "created_at", "updated_at", "is_active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity")
    fields = ("name", "image", "description", "short_description", ("price", "quantity"), "category")
    readonly_fields = ("short_description", )
    ordering = ("-name", )

    search_fields = ("name", "category__name")