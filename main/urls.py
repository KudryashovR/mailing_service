from django.urls import path

from main.apps import MainConfig
from main.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = MainConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='home'),
]
