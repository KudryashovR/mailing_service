from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class OwnerRequiredMixin:
    owner_field = 'owner'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner = getattr(obj, self.owner_field)

        if owner != request.user:
            if not request.user.is_authenticated:
                login_url = reverse('users:login')
                query_string = urlencode({'next': request.path})
                redirect_url = f"{login_url}?{query_string}"
                messages.info(request, 'Требуется аутентификация!')

                return HttpResponseRedirect(redirect_url)
            else:
                messages.info(request, 'Доступ запрещен!')

                return redirect('main:home')
        elif not request.user.is_email_verified:
            messages.info(request, 'Пожалуйста, подтвердите вашу почту!')

            return redirect('main:home')

        return super().dispatch(request, *args, **kwargs)


class EmailVerificationRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user:login')

        if not request.user.is_email_verified:
            messages.info(request, "Пожалуйста, подтвердите ваш email, чтобы получить доступ к этой странице.")

            return redirect('main:home')

        return super().dispatch(request, *args, **kwargs)


class StaffOrOwnerRequiredMixin:
    owner_field = 'owner'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner = getattr(obj, self.owner_field)
        model_name = obj._meta.model_name

        if isinstance(self, ListView) or isinstance(self, DetailView):
            perm = 'view'
        elif isinstance(self, CreateView):
            perm = 'add'
        elif isinstance(self, UpdateView):
            perm = 'change'
        elif isinstance(self, DeleteView):
            perm = 'delete'

        if (not request.user.is_staff and request.user != owner) and not request.user.has_perm(
                f'main.{perm}_{model_name}'):
            print(request.user.is_staff, request.user, owner, request.user.has_perm(f'main.{perm}_{model_name}'))
            messages.info(request, "Доступ запрещен.")

            return redirect('main:home')

        return super().dispatch(request, *args, **kwargs)
