from django.db import models
from authapp.models import User  # внешний ключ пользователь
from mainapp.models import Product  # внешний ключ продукт
from core.models import TimeStampedModel

class Basket(TimeStampedModel):
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ("created_at", "user")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт {self.product.name}"

    @property
    def baskets(self):
        return Basket.objects.filter(user=self.user)

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)