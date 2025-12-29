from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя")
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""
            field.widget.attrs.update({
                'class': 'form-control'
            })
