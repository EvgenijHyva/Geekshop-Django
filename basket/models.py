from django.db import models
from authapp.models import User  # внешний ключ пользователь
from mainapp.models import Product  # внешний ключ продукт

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # при удалении пользователя удаляются и все товары
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт {self.product.name}"

    def sum(self):
        return self.quantity * self.product.price