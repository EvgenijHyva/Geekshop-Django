from django.shortcuts import render, HttpResponseRedirect
# чтобы тользоваться формами нужно их импортировать
from authapp.forms import UserLoginForm, UserRegisterform
# так же нужно импортировать модель для работы с ней
from authapp.models import User
from django.contrib import auth
from django.urls import reverse


def login(request):
    # авторизация пользователя
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            print(user.__dict__)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("index"))

    else:
        form = UserLoginForm()
    content = {
        "form": form,
        "title": "GeekShop - Авторизация"
    }
    return render(request, "authapp/login.html", content)


def register(request):
    if request.method == 'POST':
        form = UserRegisterform(data=request.POST)
        if form.is_valid():
            form.save()  # метод сохраняет данные формы в БД
            return HttpResponseRedirect(reverse("auth:login"))
        else:
            print(form.errors)
    else:
        form = UserRegisterform()
    content = {
        "form": form,
        "title": "GeekShop - Регистрация"
    }
    return render(request, "authapp/register.html", content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


# контроллер личного кабинета:
def profile(request):
    content = {
        "title": "GeekShop - профиль"
    }
    return render(request, "authapp/profile.html", content)