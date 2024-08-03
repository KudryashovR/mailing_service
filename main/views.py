from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .mixins import OwnerRequiredMixin, EmailVerificationRequiredMixin, StaffOrOwnerRequiredMixin
from .models import Mailing, MailingAttempt, Client, BlogPost
from .forms import MailingForm, ClientForm


def index(request, *args, **kwargs):
    """
    Представление для главной страницы.

    Параметры:
        request (HttpRequest): Объект запроса Django.
        args (list): Дополнительные позиционные аргументы.
        kwargs (dict): Дополнительные именованные аргументы.

    Контекст:
        total_mailings (int): Общее количество рассылок, полученное с помощью функции `Mailing.get_total_mailings()`.
        active_mailings (int): Количество активных рассылок, полученное с помощью функции
                               `Mailing.get_active_mailings()`.
        unique_clients (int): Количество уникальных клиентов, полученное с помощью функции
                              `Client.get_unique_clients()`.
        random_articles (QuerySet): Список случайных статей блога, полученных с помощью функции
                                    `BlogPost.get_random_articles(3)`.
        current_url_name (str): Название текущего URL для использования в шаблоне, здесь 'home'.

    Возвращает:
        HttpResponse: Ответ, содержащий отрендеренный шаблон 'main/index.html' с переданным контекстом.
    """

    total_mailings = Mailing.get_total_mailings()
    active_mailings = Mailing.get_active_mailings()
    unique_clients = Client.get_unique_clients()
    random_articles = BlogPost.get_ramdom_articles(3)

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_articles': random_articles,
        'current_url_name': 'home'
    }

    return render(request,'main/index.html', context)


class MailingListView(EmailVerificationRequiredMixin, ListView):
    """
    Представление для отображения списка рассылок.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        context_object_name (str): Имя переменной контекста для списка объектов.

    Методы:
        get_context_data(self, **kwargs) -> dict: Дополняет контекст текущим URL именем.
    """

    model = Mailing
    template_name = 'main/mailing_list.html'
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.resolver_match:
            context['current_url_name'] = self.request.resolver_match.url_name
        else:
            context['current_url_name'] = None

        return context


class MailingDetailView(LoginRequiredMixin, StaffOrOwnerRequiredMixin, DetailView):
    """
    Представление для отображения деталей конкретной рассылки.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        context_object_name (str): Имя переменной контекста для объекта.
    """

    model = Mailing
    template_name = 'main/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(LoginRequiredMixin, EmailVerificationRequiredMixin, CreateView):
    """
    Представление для создания новой рассылки.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        form_class (Form): Форма, используемая для создания объекта.
        success_url (str): URL для перенаправления после успешного создания.

    Методы:
        get_context_data(self, **kwargs) -> dict: Дополняет контекст текущим URL именем.
        """
    model = Mailing
    template_name = 'main/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.resolver_match:
            context['current_url_name'] = self.request.resolver_match.url_name
        else:
            context['current_url_name'] = None

        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    """
    Представление для обновления существующей рассылки.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        form_class (Form): Форма, используемая для обновления объекта.

    Методы:
        get_success_url(self) -> str: Возвращает URL для перенаправления после успешного обновления.
        """
    model = Mailing
    template_name = 'main/mailing_form.html'
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy('main:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    """
    Представление для удаления существующей рассылки.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        success_url (str): URL для перенаправления после успешного удаления.
    """
    model = Mailing
    template_name = 'main/mailing_confirm_delete.html'
    success_url = reverse_lazy('main:home')


class MailingAttemptListView(LoginRequiredMixin, EmailVerificationRequiredMixin, ListView):
    """
    Представление для отображения списка попыток рассылки.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        context_object_name (str): Имя переменной контекста для списка объектов.
        queryset (QuerySet): Запрос, используемый для выборки данных.

    Методы:
        get_context_data(self, **kwargs) -> dict: Дополняет контекст текущим URL именем.
    """
    model = MailingAttempt
    template_name = 'main/mailing_attempt_list.html'
    context_object_name = 'mailings_attempts'
    queryset = MailingAttempt.objects.all().order_by('-time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.resolver_match:
            context['current_url_name'] = self.request.resolver_match.url_name
        else:
            context['current_url_name'] = None

        return context


class ClientListView(LoginRequiredMixin, EmailVerificationRequiredMixin, ListView):
    """
    Представление для отображения списка клиентов.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        context_object_name (str): Имя переменной контекста для списка объектов.

    Методы:
        get_context_data(self, **kwargs) -> dict: Дополняет контекст текущим URL именем.
    """
    model = Client
    template_name = 'main/client_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.resolver_match:
            context['current_url_name'] = self.request.resolver_match.url_name
        else:
            context['current_url_name'] = None

        return context


class ClientDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    """
    Представление для отображения деталей конкретного клиента.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        context_object_name (str): Имя переменной контекста для объекта.
    """

    model = Client
    template_name = 'main/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(LoginRequiredMixin, EmailVerificationRequiredMixin, CreateView):
    """
    Представление для создания нового клиента.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        form_class (Form): Форма, используемая для создания объекта.
        success_url (str): URL для перенаправления после успешного создания.

    Методы:
        get_context_data(self, **kwargs) -> dict: Дополняет контекст текущим URL именем.
    """

    model = Client
    template_name = 'main/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('main:clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.resolver_match:
            context['current_url_name'] = self.request.resolver_match.url_name
        else:
            context['current_url_name'] = None

        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    """
    Представление для обновления существующего клиента.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        form_class (Form): Форма, используемая для обновления объекта.

    Методы:
        get_success_url(self) -> str: Возвращает URL для перенаправления после успешного обновления.
    """

    model = Client
    template_name = 'main/client_form.html'
    form_class = ClientForm

    def get_success_url(self):
        return reverse_lazy('main:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    """
    Представление для удаления существующего клиента.

    Атрибуты:
        model (Model): Модель, с которой будет работать представление.
        template_name (str): Имя используемого шаблона.
        success_url (str): URL для перенаправления после успешного удаления.
    """

    model = Client
    template_name = 'main/client_confirm_delete.html'
    success_url = reverse_lazy('main:clients')


class BlogListView(ListView):
    """
    Представление для отображения списка постов блога с поддержкой пагинации.

    Атрибуты класса:
        model (Model): Модель, используемая для получения списка постов (здесь BlogPost).
        paginate_by (int): Количество постов на одной странице (здесь 8).
        ordering (str): Поле и порядок сортировки постов (здесь '-published_date', что означает сортировку по убыванию
                        даты публикации).
    """

    model = BlogPost
    paginate_by = 8
    ordering = '-published_date'

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст шаблона.

        Параметры:
            kwargs (dict): Дополнительные именованные аргументы.

        Возвращает:
            context (dict): Контекст с дополнительными данными. Включает:
                - current_url_name (str): Название текущего URL, если оно доступно; иначе None.
        """

        context = super().get_context_data(**kwargs)

        if self.request.resolver_match:
            context['current_url_name'] = self.request.resolver_match.url_name
        else:
            context['current_url_name'] = None

        return context


class BlogDetailView(DetailView):
    """
    Представление для отображения деталей отдельного поста блога.

    Атрибуты класса:
        model (Model): Модель, используемая для получения детали поста (здесь BlogPost).
    """

    model = BlogPost

    def get_object(self, *args, **kwargs):
        """
        Получает объект поста и увеличивает счетчик просмотров.

        Параметры:
            args (tuple): Дополнительные позиционные аргументы.
            kwargs (dict): Дополнительные именованные аргументы.

        Возвращает:
            article (BlogPost): Объект поста с увеличенным счетчиком просмотров.

        Сохраняет изменения в базе данных, увеличивая значение поля view_count на 1.
        """

        article = super().get_object(*args, **kwargs)

        article.view_count += 1
        article.save()

        return article


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление для создания нового поста в блоге.

    Наследуемые классы:
        LoginRequiredMixin: Проверьте, что пользователь аутентифицирован.
        PermissionRequiredMixin: Проверьте, что у пользователя есть необходимые разрешения.
        CreateView: Обработчик для создания новых объектов.

    Атрибуты класса:
        model (Model): Модель, используемая для создания нового поста (здесь BlogPost).
        fields (tuple): Поля, которые должны быть включены в форму создания поста.
        success_url (str): URL-адрес, на который перенаправляется пользователь после успешного создания поста.
        permission_required (str): Строка, представляющая необходимое разрешение для создания нового поста.
    """

    model = BlogPost
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('main:blog')
    permission_required = 'main.add_blogpost'

    def form_valid(self, form):
        """
        Устанавливает текущего пользователя как владельца создаваемого поста.

        Параметры:
            form (Form): Форма для создания нового поста.

        Возвращает:
            HttpResponseRedirect: Перенаправляет пользователя на success_url при успешной отправке формы.

        Переопределение метода для добавления текущего пользователя как владельца поста перед сохранением.
        """

        form.instance.owner = self.request.user

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Представление для обновления существующего поста в блоге.

    Наследуемые классы:
        LoginRequiredMixin: Проверяет, что пользователь аутентифицирован.
        PermissionRequiredMixin: Проверяет, что у пользователя есть необходимые разрешения.
        UpdateView: Обработчик для обновления существующих объектов.

    Атрибуты класса:
        model (Model): Модель, используемая для обновления поста (здесь BlogPost).
        fields (tuple): Поля, которые должны быть включены в форму обновления поста.
        permission_required (str): Строка, представляющая необходимое разрешение для обновления поста.
    """

    model = BlogPost
    fields = ('title', 'content', 'image')
    permission_required = 'main.change_blogpost'

    def get_success_url(self):
        """
        Возвращает URL-адрес для перенаправления пользователя после успешного обновления поста.

        Возвращает:
            str: Строка URL-адреса, на который будет перенаправлен пользователь. Здесь это детальная страница
                 обновленного поста.
        """

        return reverse_lazy('main:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления существующего поста в блоге.

    Наследуемые классы:
        LoginRequiredMixin: Проверяет, что пользователь аутентифицирован.
        PermissionRequiredMixin: Проверяет, что у пользователя есть необходимые разрешения.
        DeleteView: Обработчик для удаления существующих объектов.

    Атрибуты класса:
        model (Model): Модель, используемая для удаления поста (здесь BlogPost).
        success_url* (str): URL-адрес, на который будет перенаправлен пользователь после успешного удаления поста.
                            В данном случае это список всех постов блога.
        permission_required (str): Строка, представляющая необходимое разрешение для удаления поста.
    """

    model = BlogPost
    success_url = reverse_lazy('main:blog')
    permission_required = 'main.delete_blogpost'


@permission_required('main.set_status_disregard')
def set_mailing_status_disregard(request, mailing_id):
    """
    Изменение статуса рассылки на 'disregard'

    Проверка прав:
        Требуется наличие разрешения 'main.set_status_disregard' у пользователя.

    Параметры:
        - request (HttpRequest): Объект HTTP-запроса.
        - mailing_id (int): Идентификатор рассылки, статус которой требуется изменить.

    Возвращает:
        HttpResponseRedirect: Перенаправляет на страницу со списком всех рассылок.

    Описание:
        Данная функция получает объект рассылки по идентификатору `mailing_id`. Если объект существует, его статус
        изменяется на 'disregard'. После изменения статуса пользователь перенаправляется на страницу со списком всех
        рассылок.

    Исключения:
        - Http404: Будет вызвано, если объект рассылки с заданным идентификатором не найден.
    """

    mailing = get_object_or_404(Mailing, pk=mailing_id)
    mailing.set_status_disregard()

    return redirect('main:mailings')
