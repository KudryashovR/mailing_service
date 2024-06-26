from datetime import datetime

from django import forms
from .models import Mailing, Client


class MailingForm(forms.ModelForm):
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
