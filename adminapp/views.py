from django.shortcuts import render
from authapp.models import User


def index(request):
    context = {
        "title": "GeekShop - Admin"
    }
    return render(request, "adminapp/index.html", context)


def admin_users_read(request):
    context = {
        "title": "GeekShop - Admin",
        "users": User.objects.all()  # подтягивает всех юзеров из БД
    }
    return render(request, "adminapp/admin-users-read.html", context)
