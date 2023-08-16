from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing.forms import MailingForm
from mailing.models import Mailing, Massage


def main(request):
    """
        Переходит на страницу "Главная"
        """
    return render(request, 'mailing/main.html', )


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:main')


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing')
