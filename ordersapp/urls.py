from ordersapp.apps import OrdersappConfig
from django.urls import path


app_name = OrdersappConfig.name

def test(r):
    return r


urlpatterns = (
    path("", test, name="orders_list"),
    path("forming/complete/<int:pk>/",test, name="order_forming_complete"),
    path("create/", test, name="order_create"),
    path("read/<int:pk>/", test, name="order_read"),
    path("update/<int:pk>/", test, name="order_update"),
    path("delete/<int:pk>/", test, name="order_delete")
)