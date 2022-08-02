from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from authapp.models import User
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    context = {
        "title": "GeekShop - Admin main"
    }
    return render(request, "adminapp/index.html", context)


class UserListView(ListView):
    """список пользователей для страницы adminapp/admin-users-read.html"""
    model = User  # модель с которой работаем "Пользователи"
    template_name = "adminapp/admin-users-read.html"  # передаем параметр отвечающий за шаблон

    """что бы повесить декоратор на метод класса нужно вызвать декоратор method_decorator для класса"""
    @method_decorator(user_passes_test(lambda u : u.is_superuser))  # отображает страницу только для суперюзера
    def dispatch(self, request, *args, **kwargs):  # родительский метод работающий на отображение
        return super(UserListView, self).dispatch(request, *args, **kwargs)  # подтягиваем логику из род.класса

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(object_list=None, **kwargs)
        context["title"] = "GeekShop - Admin"
        return context


class UserCreateView(CreateView):
    """Наследуемся от Класса CreateView работает так же как admin_users_create"""
    model = User
    template_name = "adminapp/admin-users-create.html"
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy("admins:admin_users_read")

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context.update({"title": "GeekShop - Admin create user"})
        return context


class UserUpdateView(UpdateView):
    model = User
    template_name = "adminapp/admin-users-update-delete.html"
    success_url = reverse_lazy("admins:admin_users_read")
    form_class = UserAdminProfileForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

    """метод для работы с контекстом"""
    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context.update({"title" : "GeekShop - Update " + str(context["user"])})
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = "adminapp/admin-users-update-delete.html"
    success_url = reverse_lazy("admins:admin_users_read")

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object() # работает со всеми обьектами, поэтому универсальный метод для всех
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def admin_users_read(request):
    context = {
        "title": "GeekShop - Admin users",
        "users": User.objects.all()  # подтягивает всех юзеров из БД
    }
    return render(request, "adminapp/admin-users-read.html", context)


@user_passes_test(lambda u: u.is_superuser)
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
        "title": "GeekShop - Admin create user",
        "form": form
    }
    return render(request, "adminapp/admin-users-create.html", context)


@user_passes_test(lambda u: u.is_superuser)
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
        "title": "GeekShop - Admin update user",
        "form": form,
        "selected_user": user
    }
    return render(request, "adminapp/admin-users-update-delete.html", context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_delete(request, id):
    user = User.objects.get(id=id)
    if user.is_superuser:
        messages.warning(request, "superuser cant be deleted")
    else:
        # user.delete()
        user.is_active = False
        user.save()
        messages.warning(request, f"удален пользователь {user.username}")
    return HttpResponseRedirect(reverse("admins:admin_users_read"))


def admin_products(request):
    context = {
        "title": "GeekShop - Admin-products",
    }
    return render(request, "adminapp/admin_product.html", context)


def admin_categories(request):
    context = {
        "title": "GeekShop - Admin-categories"
    }
    return render(request, "adminapp/admin_categories.html", context)
