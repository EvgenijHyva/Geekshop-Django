from django.shortcuts import render, HttpResponseRedirect
# чтобы тользоваться формами нужно их импортировать
from authapp.forms import UserLoginForm, UserRegisterform, UserProfileForm
# так же нужно импортировать модель для работы с ней
from authapp.models import User
from django.contrib import auth
from django.urls import reverse
from basket.models import Basket
from django.contrib import messages  # выводит сообщения если операция успешна или нет

def login(request):
    # авторизация пользователя
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            print(user.__dict__)
            #messages.success(request, "Вы успешно авторизовались")
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
    total_quantity = 0
    total_sum = 0
    baskets = Basket.objects.filter(user=request.user)
    for basket in baskets:
        total_quantity += basket.quantity
        total_sum += basket.sum()
    content = {
        "title": "GeekShop - профиль",
        "form": form,
        "baskets": baskets,  # фильтрация по пользователю из всех корзин
        "total_quantity": total_quantity,
        "total_sum": total_sum
    }
    return render(request, "authapp/profile.html", content)