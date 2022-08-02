from django.contrib import admin
from basket.models import Basket


@admin.register(Basket)
class AdminBasket(admin.ModelAdmin):
    readonly_fields = ("created_at", "total_price")
    ordering = ("pk", "product",)
    search_fields = ("user",)
    list_display = ("user", "product", "quantity", "created_at", "total_price")

    def total_price(self, obj):
        return f"{obj.product.price * obj.quantity} руб"
