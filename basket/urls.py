from django.urls import path
from basket.views import basket_add, basket_remove, basket_edit

app_name = "basket"

urlpatterns = [
    path("basket_add/<int:product_id>/", basket_add, name="basket_add"),
    path("basket_remove/<int:id>/", basket_remove, name="basket_remove"),
    path("edit/<int:id>/<int:quantity>/", basket_edit, name="basket_edit")  # http://localhost:8000/baskets/edit/31/3/
    # должен совпасть с ссылкой в ниже! baskets берется из namespace в geekshop/urls.py
]