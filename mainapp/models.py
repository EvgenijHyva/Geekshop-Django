from django.db import models
from core.models import TimeStampedModel


class ProductCategory(TimeStampedModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name", "pk")

    name = models.CharField(max_length=64, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    is_active = models.BooleanField(verbose_name="существует", default=True)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name", "pk")

    name = models.CharField(max_length=256, verbose_name="Название продукта")
    image = models.ImageField(upload_to="products_images", blank=True, null=True, verbose_name="Изображения")
    description = models.TextField(blank=True, verbose_name="Описание")
    short_description = models.CharField(max_length=64, blank=True, verbose_name="Краткое описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="существует", default=True)

    def __str__(self):
        return f"{self.name} | {self.category.name}"
