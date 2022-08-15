from django.db import models
from core.models import TimeStampedModel
from django.conf import settings


class Order(TimeStampedModel):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("updated_at", "created_at", "pk")

    FORMING = "FM"
    SEND_TO_PROCEED = "STP"
    PROCEEDED = "PRD"
    PAID = "PD"
    CANCEL = "CNС"
    READY = "RDY"

    ORDER_STATUS_CHOICES = (
        (FORMING, "Формирование заказа"), (SEND_TO_PROCEED, "Отправлен на обработку"), (PAID, "Оплачен"),
        (CANCEL, "Отменен"), (PROCEEDED, "Обработан"), (READY, "Готов")
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    is_active = models.BooleanField(default=True, null=True, blank=True, verbose_name="Активен")
    status = models.CharField(default=FORMING, max_length=3, choices=ORDER_STATUS_CHOICES, verbose_name="Статус")

    def __str__(self):
        return f"{self.user},status:{self.status}"

    def get_total_quantity(self) -> int:
        return sum(list(map(lambda x: x.quanity, self.get_related)))

    def get_product_type_quantity(self) -> int:
        return sum(list(map(lambda x: x.quantity * x.product.price, self.get_related)))

    @property
    def get_related(self):
        return self.orderitems.select_related()

    def delete(self):
        for item in self.get_related:
            item.product.quantity -= item.quantity
            item.save()

        self.is_active = False
        self.save()


class OrderItem(TimeStampedModel):
    class Meta:
        verbose_name = "Предмет заказа"
        verbose_name_plural = "Предметы заказа"
        ordering = ("updated_at", "created_at", "pk")

    order = models.ForeignKey("Order", related_name="orderitems", on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey("mainapp.Product", verbose_name="Продукт", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="количество", default=0)

    def __str__(self):
        return f"{self.order}"

    def get_product_cost(self):
        return self.product.price * self.quantity
