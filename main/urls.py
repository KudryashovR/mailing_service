from django.urls import path

from main.apps import MainConfig
from main.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = MainConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='home'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
]
