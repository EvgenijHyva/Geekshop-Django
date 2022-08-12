from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, ShopUserProfileForm
from django.contrib import auth
from django.urls import reverse
from django.db import transaction
from authapp.models import User
from basket.models import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.utils import send_verify_mail


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
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
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                messages.success(request, f"Вы успешно зарегистрировались, письмо верификации отправлено на "
                                          f"{user.email}")
                return HttpResponseRedirect(reverse("auth:login"))
            else:
                messages.error(request, "Ошибка регистрации пользователяб, письмо верификации не отправлено")
                return HttpResponseRedirect(reverse("auth:register"))
        else:
            print(form.errors)

    else:
        form = UserRegisterForm()
    content = {
        "form": form,
        "title": "GeekShop - Регистрация"
    }
    return render(request, "authapp/register.html", content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
@transaction.atomic
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile = ShopUserProfileForm(data=request.POST, instance=request.user.shopuserprofile)
        if form.is_valid() and profile.is_valid():
            form.save()
            profile.save()
            return HttpResponseRedirect(reverse("auth:profile"))
    else:
        form = UserProfileForm(instance=request.user)
        profile = ShopUserProfileForm(instance=request.user.shopuserprofile)

    content = {
        "title": "GeekShop - профиль",
        "form": form,
        "baskets": Basket.objects.filter(user=request.user),
        "profile": profile
        # "total_quantity": sum(basket.quantity for basket in baskets),
        # "total_sum": sum(basket.sum() for basket in baskets)
    }
    return render(request, "authapp/profile.html", content)


def verify(request, email, activation_key):
    try:
        user = get_object_or_404(User, email=email)
        if (user.activation_key == activation_key) and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
        else:
            print(f"User ({user}) activation error")
            return render(request, "authapp/verification.html")
    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponseRedirect(reverse("index"))
