from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget

from .models import Mailing, Client


class MailingForm(forms.ModelForm):
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
