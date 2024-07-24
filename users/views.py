from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404

from users.forms import CustomUserCreationForm
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

    return render(request, 'users/registration.html', {'form': form})


def verify_email(request, token):
    user = get_object_or_404(User, email_verification_token=token)

    if not user.is_email_verified:
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
    else:
        messages.info(request, 'Your email was already verified.')

    return redirect('main:home')
