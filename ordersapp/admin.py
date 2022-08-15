from django.contrib import admin
from ordersapp.models import Order, OrderItem


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", )
    ordering = ("user__username", "updated_at",)
    search_fields = ("user__username", "status")
    list_display = ("username", "status", "is_active", "created_at", "updated_at", "pk")

    def username(self, obj) -> str:
        return f"{obj.user.username} {obj.user.email}"


@admin.register(OrderItem)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ("customer", "order", "product", "quantity", "cost")
    ordering = ("-pk",)
    search_fields = ("pk",)

    def customer(self, obj) -> str:
        return f"{obj.order.user.username}"

    def cost(self, obj) -> float:
        return obj.get_product_cost()
