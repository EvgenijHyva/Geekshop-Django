from django.urls import path
from authapp.views import register, login, logout, profile
from authapp.apps import AuthappConfig

app_name = AuthappConfig.name

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile")
]