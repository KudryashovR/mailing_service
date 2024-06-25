from datetime import datetime

from django import forms
from .models import Mailing


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
