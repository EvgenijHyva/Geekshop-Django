from django.urls import path
from basket.apps import BasketConfig
from basket.views import basket_add, basket_remove, basket_edit

app_name = BasketConfig.name

urlpatterns = [
    path("basket_add/<int:product_id>/", basket_add, name="basket_add"),
    path("basket_remove/<int:id>/", basket_remove, name="basket_remove"),
    path("edit/<int:id>/<int:quantity>/", basket_edit, name="basket_edit")
]