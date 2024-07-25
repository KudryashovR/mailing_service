from django.contrib.auth.views import LogoutView
from django.urls import path

from main.urls import urlpatterns as main_url
from main.apps import MainConfig
from users.views import register, verify_email, CustomLoginView, ProfileUpdateView, PasswordResetView

app_name = MainConfig.name

urlpatterns = [
                  path('register/', register, name='register'),
                  path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
                  path('login/', CustomLoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('edit_profile/', ProfileUpdateView.as_view(), name='edit_profile'),
                  path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
              ] + main_url
