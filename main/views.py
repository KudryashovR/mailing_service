from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Mailing, MailingAttempt, Client
from .forms import MailingForm, ClientForm


class MailingListView(ListView):
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


class MailingDetailView(DetailView):
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


class MailingCreateView(CreateView):
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


class MailingUpdateView(UpdateView):
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


class MailingDeleteView(DeleteView):
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


class MailingAttemptListView(ListView):
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


class ClientListView(ListView):
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
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.resolver_match:
            context['current_url_name'] = self.request.resolver_match.url_name
        else:
            context['current_url_name'] = None

        return context


class ClientDetailView(DetailView):
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


class ClientCreateView(CreateView):
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


class ClientUpdateView(UpdateView):
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


class ClientDeleteView(DeleteView):
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
