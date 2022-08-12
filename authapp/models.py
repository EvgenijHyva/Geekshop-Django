from django.utils import timezone
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser
from core.utils import get_activation_key_expiration_date
from core.models import TimeStampedModel
from django.db.models.signals import post_save


class User(AbstractUser):
    avatar = models.ImageField(upload_to="users_avatar", blank=True, verbose_name="Аватар")
    age = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Возраст")
    phone = models.CharField(max_length=20, verbose_name="телефон", blank=True)
    city = models.CharField(max_length=50, verbose_name="Город", blank=True)
    activation_key = models.CharField(max_length=128, blank=True, verbose_name="Ключ")
    activation_key_expire = models.DateTimeField(default=get_activation_key_expiration_date,
                                               verbose_name="Срок действия ключа")

    def is_activation_key_expired(self) -> bool:
        if any((self.is_staff, self.is_superuser)) and self.is_active:
            return False
        return self.activation_key_expire <= timezone.now()


class ShopUserProfile(TimeStampedModel):
    MALE = "M"
    FEMALE = "W"
    UFO = "U"
    NON_BINARY = "X"
    GENDER_CHOICES = (
        (MALE, "М"),
        (FEMALE, "Ж"),
        (UFO, "И"),
        (NON_BINARY, "Н")
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ("created_at", "user", )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE,
                                verbose_name="Пользователь")
    gender = models.CharField(verbose_name="Пол", max_length=1, blank=True, choices=GENDER_CHOICES)
    tagline = models.CharField(verbose_name="Тэги", max_length=128, blank=True, null=True)
    about = models.TextField(verbose_name="О себе", null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.shopuserprofile.save()

    def __str__(self):
        return f"{self.user.username}:({self.gender if self.gender else '-'}), id:{self.user.pk}"