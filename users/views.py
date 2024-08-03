from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import UpdateView, ListView, DetailView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm, ProfileForm
from users.models import User


def register(request):
    """
    Обработка регистрации пользователя

    Описание:
        Эта функция обрабатывает регистрацию нового пользователя. Если запрос является POST, функция проверяет данные
        формы. Если данные формы действительны, создается новый пользователь, и он сразу же автоматически входит
        в систему.  После успешной регистрации пользователь перенаправляется на домашнюю страницу. Если запрос
        не является POST, отображается пустая форма регистрации.

    Параметры:
        - request (HttpRequest): Объект запроса, полученный от клиента.

    Возвращает:
        - HttpResponse: Ответ с отрисованной страницей регистрации или перенаправление на домашнюю страницу.

    Шаблоны:
        - users/registration.html: Шаблон для страницы регистрации пользователей.

    Контекст:
        - form (CustomUserCreationForm): Форма для создания нового пользователя.
        - current_url_name (str): Текущая имя URL (в данном случае 'register') для использования в шаблоне.
    """

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('main:home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/registration.html', {'form': form,
                                                       'current_url_name': 'register'})


def verify_email(request, token):
    """
    Подтверждение электронной почты пользователя

    Описание:
        Эта функция обрабатывает подтверждение электронной почты пользователя. Находит пользователя по предоставленному
        токену. Если электронная почта пользователя ранее не была подтверждена, отмечает её как подтверждённую
        и сохраняет изменения. Если электронная почта уже подтверждена, пользователь информируется об этом.

    Параметры:
        - request (HttpRequest): Объект запроса, полученный от клиента.
        - token (str): Токен для подтверждения электронной почты, связанный с пользователем.

    Возвращает:
        - HttpResponse: Перенаправляет на домашнюю страницу.

    Сообщения:
        - messages.success: Информирует пользователя об успешном подтверждении электронной почты.
        - messages.info: Информирует пользователя о том, что электронная почта уже была подтверждена.
    """

    user = get_object_or_404(User, email_verification_token=token)

    if not user.is_email_verified:
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Почта подтверждена.')
    else:
        messages.info(request, 'Почта не требует подтверждения.')

    return redirect('main:home')


class CustomLoginView(LoginView):
    """
    Кастомизированный вид для входа пользователя

    Описание:
        Этот класс представляет собой кастомизированную версию стандартного представления для входа пользователя.
        Он задает шаблон для отображения страницы входа и добавляет дополнительный контекст к данным шаблона.

    Атрибуты:
        - template_name (str): Имя файла шаблона, который будет использоваться для отображения страницы входа.

    Методы:
        - get_context_data(self, **kwargs): Добавляет дополнительный контекст к данным шаблона.
        - form_valid(self, form): Отправляет сообщение об успешном входе после успешной аутентификации.
    """

    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        """
        Получает контекстные данные для правильного отображения шаблона.

        Описание:
            Этот метод добавляет в контекст данных шаблона дополнительный ключ 'current_url_name', который указывает
            текущее имя URL. В данном случае это 'login'.

        Параметры:
            - **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            - context (dict): Обновленный контекст с дополнительными данными
        """

        context = super().get_context_data(**kwargs)

        context['current_url_name'] = 'login'

        return context

    def form_valid(self, form):
        """
        Обрабатывает корректную отправку формы входа.

        Описание:
            Этот метод вызывается, когда форма логина валидна. Он отправляет приветственное сообщение пользователю
            после успешной аутентификации.

        Параметры:
            - form (Form): Объект формы, которая была проверена и признана валидной.

        Возвращает:
            - response: HTTP-ответ после успешной обработки формы.
        """

        response = super().form_valid(form)

        user = form.get_user()
        messages.success(self.request, f'Добро пожаловать, {user.get_full_name()}!')

        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Вью-класс для обновления профиля пользователя

    Описание:
        Этот класс представляет собой представление для обновления профиля пользователя.
        Пользователь должен быть аутентифицирован для доступа к этому представлению.
        Форма для редактирования профиля, шаблон для отображения формы и URL перенаправления после успешного обновления
        задаются в атрибутах класса.

    Атрибуты:
        - model (Model): Модель пользователя, используемая в представлении.
        - form_class (Form): Форма для редактирования профиля пользователя.
        - template_name (str): Имя файла шаблона для отображения страницы редактирования профиля.
        - success_url (str): URL, на который будет перенаправлен пользователь после успешного обновления профиля.

    Методы:
        - get_object(self): Возвращает объект текущего аутентифицированного пользователя.
    """

    model = User
    form_class = ProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('main:home')

    def get_object(self):
        """
        Возвращает объект текущего аутентифицированного пользователя.

        Описание:
            Этот метод используется для получения объекта пользователя, чей профиль будет редактироваться.
            Возвращается пользователь, чья сессия активна (текущий аутентифицированный пользователь).

        Возвращает:
            - user (User): Текущий аутентифицированный пользователь.
        """

        return User.objects.get(email=self.request.user)


class PasswordResetView(View):
    """
    Вью-класс для сброса пароля пользователя

    Описание:
        Этот класс представляет собой представление для сброса пароля пользователя. Включает методы
        для обработки GET и POST запросов. При GET запросе отображается форма для ввода email,
        а при POST запросе происходит сброс пароля и отправка нового пароля на email пользователя.

    Методы:
        - get(self, request): Обрабатывает GET запрос и возвращает HTML страницу с формой для сброса пароля.
        - post(self, request): Обрабатывает POST запрос, сбрасывает пароль пользователя и отправляет новый пароль
                               на email.
        - send_new_password_email(user, new_password): Статический метод, отправляющий электронное письмо с новым
                                                       паролем.
    """

    def get(self, request):
        """
        Обрабатывает GET запрос и возвращает HTML страницу с формой для сброса пароля.

        Аргументы:
            - request (HttpRequest): Объект запроса.

        Возвращает:
            - HttpResponse: Ответ, содержащий HTML страницу с формой для сброса пароля.
        """

        return render(request, 'users/password_reset.html')

    def post(self, request):
        """
        Обрабатывает POST запрос, сбрасывает пароль пользователя и отправляет новый пароль на email.

        Аргументы:
            - request (HttpRequest): Объект запроса, содержащий данные формы.

        Возвращает:
            - HttpResponse: Ответ с сообщением о том, что новый пароль отправлен на email пользователя.
        """

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
        """
        Статический метод, отправляющий электронное письмо с новым паролем.

        Аргументы:
            - user (User): Объект пользователя, которому отправляется письмо.
            - new_password (str): Новый пароль, который будет отправлен пользователю.

        Возвращает:
            - None
        """

        send_mail("Your new password", f"Your new password is: {new_password}", EMAIL_HOST_USER,
                  [user.email])


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Вью-класс для отображения списка пользователей

    Описание:
        Этот класс представляет собой представление для отображения списка пользователей.
        Только авторизованные пользователи с необходимыми правами могут получить доступ к этому представлению.
        Наследует LoginRequiredMixin для защиты от неавторизованных пользователей и
        PermissionRequiredMixin для проверки прав доступа.

    Атрибуты:
        - model (Model): Модель, данные которой будут отображаться в списке.
        - permission_required (str): Название права доступа, необходимого для просмотра списка пользователей.

    Методы:
        - get_context_data(self, **kwargs): Получает данные контекста для шаблона. Добавляет имя текущего URL во
          избежание ошибок, если маршрут не определяется.
    """

    model = User
    permission_required = 'users.view_user'

    def get_context_data(self, **kwargs):
        """
        Получает данные контекста для шаблона.

        Аргументы:
            - **kwargs: Дополнительные аргументы контекста.

        Возвращает:
            - dict: Словарь с данными контекста, включающий имя текущего URL (если он определен).
        """

        context = super().get_context_data(**kwargs)

        if self.request.resolver_match:
            context['current_url_name'] = self.request.resolver_match.url_name
        else:
            context['current_url_name'] = None

        return context


class UserDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Вью-класс для отображения подробной информации о пользователе

    Описание:
        Этот класс представляет собой представление для отображения подробной информации о конкретном пользователе.
        Только авторизованные пользователи с необходимыми правами могут получить доступ к этому представлению.
        Наследует LoginRequiredMixin для защиты от неавторизованных пользователей и
        PermissionRequiredMixin для проверки прав доступа.

    Атрибуты:
        - model (Model): Модель, данные которой будут отображаться.
        - permission_required (str): Название права доступа, необходимого для просмотра подробной информации
                                     о пользователе.
    """

    model = User
    permission_required = 'users.view_user'


@permission_required('users.set_active')
def toggle_user_active(request, user_id):
    """
    Представление для переключения активности пользователя

    Описание:
        Эта функция позволяет переключать состояние активности пользователя (активный/неактивный).
        Только пользователи с необходимыми правами могут выполнить эту операцию.

    Аргументы:
        - request (HttpRequest): Объект запроса.
        - user_id (int): Идентификатор пользователя, для которого будет переключаться состояние активности.

    Возвращает:
        - HttpResponseRedirect: Перенаправление на страницу со списком пользователей после выполнения операции.
    """

    user = get_object_or_404(User, pk=user_id)
    user.is_active = not user.is_active
    user.save()

    return redirect('user:users')
