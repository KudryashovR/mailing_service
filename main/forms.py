from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget

from .models import Mailing, Client


class MailingForm(forms.ModelForm):
    """
    Форма для создания и обновления экземпляров модели Mailing.

    Атрибуты:
        scheduled_time (forms.DateTimeField): Поле для указания даты и времени отправки, отображается как ввод типа
                                              datetime-local.
    """

    scheduled_time = forms.DateTimeField(label='Дата и время отправки',
                                         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Mailing
        fields = [
            'title',
            'message',
            'status',
            'scheduled_time',
            'periodicity',
            'clients'
        ]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'last_name', 'first_name', 'second_name', 'comment']
