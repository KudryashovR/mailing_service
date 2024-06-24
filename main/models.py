from django.db import models


NULLABLE = {
    'blank': True,
    'null': True
}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    second_name = models.CharField(max_length=50, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.second_name}'

    def get_initials(self):
        return f'{self.last_name} {self.first_name[0]}. {self.second_name[0]}.'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Новый', 'Новый'),
        ('Отправлен', 'Отправлен'),
        ('Отклонен', 'Отклонен'),
    ]

    title = models.CharField(max_length=255, verbose_name='Заголовок рассылки')
    message = models.TextField(verbose_name='Содержание рассылки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус рассылки', default='Новый')
    scheduled_time = models.DateTimeField(verbose_name='Дата и время отправки')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    time = models.DateTimeField(verbose_name='Дата и время попытки отправки')
    status = models.CharField(max_length=10, choices=Mailing.STATUS_CHOICES, verbose_name='Статус попытки отправки')

    def __str__(self):
        return f'Попытка отправки рассылки {self.mailing.title} на {self.time}'

    class Meta:
        verbose_name = 'Попытка отправки рассылки'
        verbose_name_plural = 'Попытки отправки рассылок'
