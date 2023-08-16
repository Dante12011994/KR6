import datetime

from django.conf import settings
from django.core.mail import send_mail
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

    def form_valid(self, form):
        if form.is_valid():
            time_now = datetime.date.today()
            self.object = form.save()
            if self.object.start <= time_now < self.object.stop:
                self.object.status_mail = 'start'
                mail = self.object.massage
                users = self.object.users_group.all()
                for user in users:
                    send_mail(
                        subject=mail.mail_subject,
                        message=mail.text,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email]
                    )
                self.object.datatime = time_now
            elif time_now > self.object.stop:
                self.object.status_mail = 'finished'
            self.object.save()
            return super().form_valid(form)


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
