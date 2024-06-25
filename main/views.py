from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Mailing, MailingAttempt
from .forms import MailingForm


class MailingListView(ListView):
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
    model = Mailing
    template_name = 'main/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
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
    model = Mailing
    template_name = 'main/mailing_form.html'
    form_class = MailingForm
    # success_url = reverse_lazy('main:home')

    def get_success_url(self):
        return reverse_lazy('main:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'main/mailing_confirm_delete.html'
    success_url = reverse_lazy('main:home')


class MailingAttemptListView(ListView):
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
