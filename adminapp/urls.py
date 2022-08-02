from django.urls import path
from adminapp.apps import AdminappConfig
from adminapp.views import index, admin_users_read, admin_users_create, admin_users_update, admin_users_delete, \
    admin_products, admin_categories, UserListView, UserCreateView, UserUpdateView, UserDeleteView

app_name = AdminappConfig.name

urlpatterns = [
    path("", index, name="index"),
    path("admin-users-read/", UserListView.as_view(), name="admin_users_read"),
    path("admin-users-create/", UserCreateView.as_view(), name="admin_users_create"),
    path("admin-users-update/<int:pk>/", UserUpdateView.as_view(), name="admin_users_update"),
    # редактирование определенного пользователя а значит передаем ID
    path("admin-users-delete/<int:pk>/", UserDeleteView.as_view(), name="admin_users_delete"),
    # удаление пользователя
    path("admin-products", admin_products, name="admin_products"),
    path("admin-categories", admin_categories, name="admin_categories")
]
