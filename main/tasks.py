import smtplib
from datetime import datetime

from django.core.mail import send_mail
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from .models import Mailing, MailingAttempt


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(
        scheduled_time__lte=current_datetime,
        status='Новый'
    )

    for mailing in mailings:
        successful = True
        for client in mailing.clients.all():
            try:
                send_mail(subject=mailing.title,
                          message=mailing.message,
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[client.email],
                          fail_silently=False,
                          )
            except smtplib.SMTPException as e:
                successful = False

                print(e)

        print(f"sending email to {client.email}...{'' if successful else 'failed'}")

        mailing.status = 'Отправлен' if successful else 'Отклонен'
        mailing.save()

        MailingAttempt.objects.create(mailing=mailing, status=mailing.status)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()
