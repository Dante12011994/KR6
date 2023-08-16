import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailing.models import Mailing


def sendmail(massage, user):
    send_mail(
        subject=massage.mail_subject,
        message=massage.text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


def start_check(mailing):
    if mailing.start == datetime.date.today():
        for user in mailing.users_group.all():
            sendmail(mailing.massage, user)
            mailing.status_mail = 'start'
            mailing.save()


def finish_check(mailing):
    for user in mailing.users_group.all():
        sendmail(mailing.massage, user)
    if mailing.stop == datetime.date.today():
        mailing.status_mail = 'finished'
        mailing.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for mailing in Mailing.objects.all():
            if mailing.status_mail == 'create':
                start_check(mailing)
            elif mailing.status_mail == 'start':
                finish_check(mailing)
