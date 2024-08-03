from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, UsernameField
from django.urls import reverse_lazy

from users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    """
    Форма для обновления профиля пользователя с функциональностью смены пароля

    Поля:
        - old_password (CharField): Старый пароль пользователя. Отображается как поле ввода пароля.
        - new_password1 (CharField): Новый пароль пользователя. Отображается как поле ввода пароля.
        - new_password2 (CharField): Подтверждение нового пароля пользователя. Отображается как поле ввода пароля.

    Методы:
        - clean(self): Проверяет совпадение нового пароля и его подтверждения.

        Если пароли не совпадают, добавляется соответствующая ошибка в поле 'new_password2'.

    Описание:
        Данная форма позволяет пользователю обновлять свой профиль, включая возможность смены пароля.
    """

    old_password = forms.CharField(widget=forms.PasswordInput, label='Старый пароль')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Подтвердите новый пароль')

    def clean(self):
        """
        Проверка совпадения нового пароля и его подтверждения

        Описание:
            Метод очищает и проверяет данные формы. Если поля 'new_password1' и 'new_password2' не совпадают,
            добавляется ошибка.

        Возвращает:
            dict: Очищенные данные формы.
        """

        cleaned_data = super().clean()

        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "Пароли не совпадают")

        return cleaned_data

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
