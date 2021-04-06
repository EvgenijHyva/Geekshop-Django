from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from authapp.models import User
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm
from django.contrib import messages  # выводит сообщения если операция успешна или нет

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


# контроллер для создания пользователя на странице admin-users-create
def admin_users_create(request):
    if request.method == "POST":
        form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно зарегестрирован!")
            return HttpResponseRedirect(reverse("admins:admin_users_read"))
        else:
            print(form.errors)
    else:
        form = UserAdminRegisterForm()
    context = {
        "title": "GeekShop - Admin",
        "form": form
    }
    return render(request, "adminapp/admin-users-create.html", context)


def admin_users_update(request, id):
    # обьект пользователя которого выбрали
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admins:admin_users_read"))
    else:
        form = UserAdminProfileForm(instance=user)
    context = {
        "title": "GeekShop - Admin",
        "form": form,
        "selected_user": user
    }
    return render(request, "adminapp/admin-users-update-delete.html", context)


# контроллер на удаление
def admin_users_delete(request, id):
    user = User.objects.get(id=id)
    #user.is_active = False
    #user.save()
    if user.is_superuser:
        messages.warning(request, "superuser cant be deleted")
    else:
        user.delete()
        messages.warning(request, f"удален пользователь {user.username}")
    return HttpResponseRedirect(reverse("admins:admin_users_read"))
