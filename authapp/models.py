from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from core.utils import get_activation_key_expiration_date


class User(AbstractUser):
    avatar = models.ImageField(upload_to="users_avatar", blank=True, verbose_name="Аватар")
    age = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Возраст")
    phone = models.CharField(max_length=20, verbose_name="телефон", blank=True)
    city = models.CharField(max_length=50, verbose_name="Город", blank=True)
    activation_key = models.CharField(max_length=128, blank=True, verbose_name="Ключ")
    activation_key_expire = models.DateTimeField(default=get_activation_key_expiration_date,
                                               verbose_name="Срок действия ключа")

    def is_activation_key_expired(self) -> bool:
        return any(not self.is_staff, not self.is_superuser, self.activation_key_expire <= datetime.now())
