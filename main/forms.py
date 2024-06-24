from django import forms
from .models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = [
            'title',
            'message',
            'status',
            'scheduled_time',
            'clients'
        ]