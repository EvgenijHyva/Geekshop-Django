from django.contrib import admin

# до регистрации нет отображения пользователей в админке
from authapp.models import User

admin.site.register(User)
