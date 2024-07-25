from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm, ProfileForm
from users.models import User


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('main:home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/registration.html', {'form': form, 'current_url_name': 'register'})


def verify_email(request, token):
    user = get_object_or_404(User, email_verification_token=token)

    if not user.is_email_verified:
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
    else:
        messages.info(request, 'Your email was already verified.')

    return redirect('main:home')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_url_name'] = 'login'

        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.get_user()
        messages.success(self.request, f'Добро пожаловать, {user.get_full_name()}!')

        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('main:home')

    def get_object(self):
        return User.objects.get(email=self.request.user)


class PasswordResetView(View):
    def get(self, request):
        return render(request, 'users/password_reset.html')

    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user:
            new_password = get_random_string(12)
            user.password = make_password(new_password)
            user.save()
            self.send_new_password_email(user, new_password)

        return HttpResponse(
            'Новый пароль отправлен на вашу почту. <a href="{0}">Назад</a>'.format(reverse_lazy('user:login')))

    @staticmethod
    def send_new_password_email(user, new_password):
        send_mail("Your new password", f"Your new password is: {new_password}", EMAIL_HOST_USER, [user.email])
