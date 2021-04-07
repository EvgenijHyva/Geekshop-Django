from django.urls import path
from mainapp.views import products

app_name = "mainapp"   # для того что бы приложение понимало с каким приложением оно работает

urlpatterns = [
    path("", products, name="index"),
    path("<int:category_id>/", products, name="product"),  # сортировка по категориям с Paginator
    path("<str:product_name>/product", products, name="some_product"),  # при нажатии на отдельный товар
    path("page/<int:page>/", products, name="page"),
]