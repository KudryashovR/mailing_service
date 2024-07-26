from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .mixins import OwnerRequiredMixin, EmailVerificationRequiredMixin, StaffRequiredMixin
from .models import Mailing, MailingAttempt, Client, BlogPost
from .forms import MailingForm, ClientForm


def index(request, *args, **kwargs):
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


class MailingDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
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
    model = BlogPost
    paginate_by = 8
    ordering = '-published_date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.resolver_match:
            context['current_url_name'] = self.request.resolver_match.url_name
        else:
            context['current_url_name'] = None

        return context


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost

    def get_object(self, *args, **kwargs):
        article = super().get_object(*args, **kwargs)

        article.view_count += 1
        article.save()

        return article


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('main:blog')
    permission_required = 'main.add_blogpost'

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPost
    fields = ('title', 'content', 'image')
    permission_required = 'main.change_blogpost'

    def get_success_url(self):
        return reverse_lazy('main:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('main:blog')
    permission_required = 'main.delete_blogpost'


@permission_required('main.set_status_disregard')
def set_mailing_status_disregard(request, mailing_id):
    mailing = get_object_or_404(Mailing, pk=mailing_id)
    mailing.set_status_disregard()

    return redirect('main:mailings')
