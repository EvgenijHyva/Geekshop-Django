from django.urls import path
from mainapp.views import products, products_by_category

app_name = "mainapp"   # для того что бы приложение понимало с каким приложением оно работает

urlpatterns = [
    # path("products/", mainapp_views.products, name="products") меняется

    path("", products, name="index"),
    path("<int:id>", products, name="product"),  # для шаблона: /products/1
    path("category/<int:category_id>", products_by_category, name="products_by_category"),
]