from django.urls import path
from mainapp.apps import MainappConfig
from mainapp.views import products

app_name = MainappConfig.name

urlpatterns = [
    path("", products, name="index"),
    path("<int:category_id>/", products, name="product"),
    path("<str:product_name>/product", products, name="some_product"),
    path("page/<int:page>/", products, name="page"),
]