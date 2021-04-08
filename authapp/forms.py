from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    # дополнительные параметры:
    def __init__(self, *args, **kwargs):  # переопределяя метод нужно указать
        super(UserLoginForm, self).__init__(*args, **kwargs)  # все переменные что было созданы выше их нужно
        # использовать

        self.fields["username"].widget.attrs['placeholder'] = "Введите имя пользователя"  # добавим placeholder
        self.fields["password"].widget.attrs['placeholder'] = "Введите пароль"
        # добавим класс в input циклом for:
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control py-4"


class UserRegisterform(UserCreationForm):  # форма регистрации register.html
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegisterform, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs['placeholder'] = "Введите имя пользователя"
        self.fields["email"].widget.attrs['placeholder'] = "Введите адрес эл. почты"
        self.fields["first_name"].widget.attrs['placeholder'] = "Введите имя"
        self.fields["last_name"].widget.attrs['placeholder'] = "Введите фамилию"
        self.fields["password1"].widget.attrs['placeholder'] = "Введите пароль"
        self.fields["password2"].widget.attrs['placeholder'] = "Повторите пароль"
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control py-4"
            field.help_text = ''


class UserProfileForm(UserChangeForm):  # форма обновления информации в profile.html
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:  # добавим поля которые для обновления и которые служат для отображения
        model = User
        fields = ("first_name", "last_name", "avatar", "username", "email")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control py-4"

        self.fields['username'].widget.attrs['readonly'] = True  # поле только для чтения
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields["avatar"].widget.attrs["class"] = "custom-file-input"