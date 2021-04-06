from django import forms
from authapp.forms import UserRegisterform, UserProfileForm
from authapp.models import User

# приложение adminapp регистрирование пользователя через админ-панель
class UserAdminRegisterForm(UserRegisterform):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2", "avatar")

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)  # вызываем поля класса UserRegisterform
        self.fields["avatar"].widget.attrs["class"] = "custom-file-input"  # дополняем унаследованный класс новым полем


# приложение adminapp обновление и удаление информации пользователя через админ-панель
class UserAdminProfileForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        # изменяем поля (username, email) на возможность редактирования,
        # ps. эти поля в классе профиля были закрыты
        self.fields["username"].widget.attrs["readonly"] = False
        self.fields["email"].widget.attrs["readonly"] = False



