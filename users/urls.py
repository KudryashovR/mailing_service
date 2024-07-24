from django.urls import path

from main.apps import MainConfig
from users.views import register, verify_email

app_name = MainConfig.name

urlpatterns = [
    path('register/', register, name='register'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
]
