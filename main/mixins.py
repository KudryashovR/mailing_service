from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode


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

        return super().dispatch(request, *args, **kwargs)
