import smtplib
from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from .models import Mailing, MailingAttempt


def send_mailing():
    """
    Функция для отправки запланированных рассылок клиентам.

    Функция выполняет следующие действия:
        1. Определяет текущую дату и время в заданной временной зоне.
        2. Получает все рассылки, запланированные на текущее время или ранее.
        3. Для каждой найденной рассылки:
            - Отправляет сообщение всем клиентам, привязанным к данной рассылке.
            - Записывает попытки отправки в базу данных.
            - Обновляет статус рассылки в зависимости от успешности отправки.
            - Если рассылка была успешной, обновляет время следующей запланированной отправки в зависимости
              от периодичности.
        4. Сохраняет изменения в базе данных.

    Исключения:
        smtplib.SMTPException: Ловит исключения SMTP при отправке письма и записывает их в лог сообщения.

    Возвращает:
        None
    """

    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(scheduled_time__lte=current_datetime)

    if not mailings.exists():
        return

    for mailing in mailings:
        if mailing.status == 'Отклонен':
            continue

        clients = mailing.clients.all()
        successful = True

        for client in clients:
            try:
                send_mail(subject=mailing.title,
                          message=mailing.message,
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[client.email],
                          fail_silently=False)
                MailingAttempt.objects.create(mailing=mailing, status='Отправлен',
                                              log_message=f'Успешная отправка на {client.email}')

            except smtplib.SMTPException as e:
                successful = False
                MailingAttempt.objects.create(mailing=mailing, status='Отклонен', log_message=str(e))

        mailing.status = 'Отправлен' if successful else 'Отклонен'

        if successful:
            match mailing.periodicity:
                case 'Ежедневно':
                    mailing.scheduled_time = current_datetime + timedelta(days=1)
                case 'Еженедельно':
                    mailing.scheduled_time = current_datetime + timedelta(days=7)
                case 'Ежемесячно':
                    mailing.scheduled_time = current_datetime + timedelta(days=30)

        mailing.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()
