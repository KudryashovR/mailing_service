from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class OwnerRequiredMixin:
    """
    Миксин для проверки прав владельца объекта и аутентификации пользователя.

    Атрибуты:
        owner_field (str): Имя поля модели, которое содержит владельца объекта.
    """

    owner_field = 'owner'

    def dispatch(self, request, *args, **kwargs):
        """
        Переопределяет метод dispatch для проверки прав владельца объекта.

        Параметры:
            request (HttpRequest): Объект запроса.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse: Перенаправляет пользователя на страницу логина или домашнюю страницу, если проверка владельца
                          или аутентификации не пройдена, либо вызывает метод dispatch родительского класса.
        """

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
    """
    Миксин для проверки верификации email пользователя.

    Методы:
        dispatch (HttpRequest, *args, **kwargs): Переопределяет метод dispatch для проверки верификации email
                                                 пользователя и аутентификации.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Переопределяет метод dispatch для проверки верификации email пользователя.

        Параметры:
            request (HttpRequest): Объект запроса.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse: Перенаправляет пользователя на страницу логина, домашнюю страницу, если проверка верификации
                          email или аутентификации не завершена, либо вызывает метод dispatch родительского класса.
        """

        if not request.user.is_authenticated:
            return redirect('user:login')

        if not request.user.is_email_verified:
            messages.info(request, "Пожалуйста, подтвердите ваш email, чтобы получить доступ к этой странице.")

            return redirect('main:home')

        return super().dispatch(request, *args, **kwargs)


class StaffOrOwnerRequiredMixin:
    """
    Миксин для проверки прав доступа пользователя как сотрудника или владельца объекта.

    Атрибуты:
        owner_field (str): Имя поля, содержащего информацию о владельце объекта.

    Методы:
        dispatch (HttpRequest, *args, **kwargs): Переопределяет метод dispatch для проверки прав доступа пользователя.
    """

    owner_field = 'owner'

    def dispatch(self, request, *args, **kwargs):
        """
        Переопределяет метод dispatch для проверки прав доступа пользователя как сотрудника или владельца объекта.

        Параметры:
            request (HttpRequest): Объект запроса.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse: Перенаправляет пользователя на домашнюю страницу, если у него нет необходимых прав доступа,
                          либо вызывает метод dispatch родительского класса.
        """

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
            messages.info(request, "Доступ запрещен.")

            return redirect('main:home')

        return super().dispatch(request, *args, **kwargs)
