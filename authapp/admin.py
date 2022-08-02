from django.contrib import admin
from authapp.models import User


@admin.register(User)
class AdminShopUser(admin.ModelAdmin):
    readonly_fields = ("date_joined", "id")
    ordering = ("username", "id", "is_superuser")
    search_fields = ("username", "first_name", "last_name")
    list_display = ("username", "email", "is_superuser", "is_staff", "is_active", "date_joined")
