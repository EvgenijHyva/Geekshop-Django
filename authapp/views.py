from django.shortcuts import render, HttpResponseRedirect
# чтобы тользоваться формами нужно их импортировать
from authapp.forms import UserLoginForm, UserRegisterform, UserProfileForm
# так же нужно импортировать модель для работы с ней
from authapp.models import User
from django.contrib import auth
from django.urls import reverse
from basket.models import Basket
from django.contrib import messages  # выводит сообщения  если операция успешна или нет
from django.contrib.auth.decorators import login_required


def login(request):
    # авторизация пользователя
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            # print(user.__dict__)
            # messages.success(request, "Вы успешно авторизовались")
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("products:index"))

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
            messages.success(request, "Вы успешно зарегистрировались")  # при регистрации
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
@login_required
def profile(request):
    # обновление данных!!!
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)  # для работы с
        # изображениями files
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("auth:profile"))
    # просто заходим в личный кабинет проверить данные
    else:
        form = UserProfileForm(instance=request.user)

    content = {
        "title": "GeekShop - профиль",
        "form": form,
        "baskets": Basket.objects.filter(user=request.user),  # фильтрация по пользователю из всех корзин
        # "total_quantity": sum(basket.quantity for basket in baskets),
        # "total_sum": sum(basket.sum() for basket in baskets)
    }
    return render(request, "authapp/profile.html", content)
