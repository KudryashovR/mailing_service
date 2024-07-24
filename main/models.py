from django.db import models

from users.models import User

NULLABLE = {
    'blank': True,
    'null': True
}


class Client(models.Model):
    """
    Модель представляет клиента.

    Атрибуты:
        email (models.EmailField): Электронная почта клиента, обязательное поле, уникальное.
        last_name (models.CharField): Фамилия клиента, обязательное поле, максимальная длина 50 символов.
        first_name (models.CharField): Имя клиента, обязательное поле, максимальная длина 50 символов.
        second_name (models.CharField): Отчество клиента, необязательное поле, максимальная длина 50 символов.
        comment (models.TextField): Комментарий к клиенту, необязательное поле.

    Методы:
        get_full_name(): Возвращает полное имя клиента.
        get_initials(): Возвращает инициалы клиента.
    """

    email = models.EmailField(unique=True, verbose_name='Email')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    second_name = models.CharField(max_length=50, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        """
        Строковое представление объекта Client, возвращает полное имя клиента.

        Возвращает:
            str: Полное имя клиента.
        """

        return self.get_full_name()

    def get_client_owner(self):
        return self.owner

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def get_full_name(self):
        """
        Возвращает полное имя клиента.

        Возвращает:
            str: Полное имя клиента в формате 'Фамилия Имя Отчество'.
        """

        return f'{self.last_name} {self.first_name} {self.second_name}'

    def get_initials(self):
        """
        Возвращает инициалы клиента.

        Возвращает:
            str: Инициалы клиента в формате 'Фамилия И. О.'.
        """

        return f'{self.last_name} {self.first_name[0]}. {self.second_name[0]}.'


class Mailing(models.Model):
    """
    Модель представляет рассылку.

    Перечисления:
        STATUS_CHOICES (list): Список возможных статусов рассылки.
        PERIODICITY_CHOICES (list): Список возможных периодичностей рассылки.

    Атрибуты:
        title (models.CharField): Заголовок рассылки, обязательное поле, максимальная длина 255 символов.
        message (models.TextField): Содержание рассылки, обязательное поле.
        status (models.CharField): Статус рассылки, обязательное поле, максимальная длина 10 символов, по умолчанию
                                   'Новый'.
        scheduled_time (models.DateTimeField): Дата и время отправки рассылки, обязательное поле.
        periodicity (models.CharField): Периодичность рассылки, обязательное поле, максимальная длина 15 символов,
                                        по умолчанию 'Ежедневно'.
        clients (models.ManyToManyField): Список клиентов, которым будет отправлена рассылка.
    """

    STATUS_CHOICES = [
        ('Новый', 'Новый'),
        ('Отправлен', 'Отправлен'),
        ('Отклонен', 'Отклонен'),
    ]
    PERIODICITY_CHOICES = [
        ('Ежедневно', 'Ежедневно'),
        ('Еженедельно', 'Еженедельно'),
        ('Ежемесячно', 'Ежемесячно'),
    ]

    title = models.CharField(max_length=255, verbose_name='Заголовок рассылки')
    message = models.TextField(verbose_name='Содержание рассылки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус рассылки', default='Новый')
    scheduled_time = models.DateTimeField(verbose_name='Дата и время отправки')
    periodicity = models.CharField(max_length=15, choices=PERIODICITY_CHOICES, verbose_name='Периодичность расылки',
                                   default='Ежедневно')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailing')

    def __str__(self):
        """
        Строковое представление объекта Mailing, возвращает заголовок рассылки.

        Возвращает:
            str: Заголовок рассылки.
        """

        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingAttempt(models.Model):
    """
    Модель представляет попытку отправки рассылки.

    Атрибуты:
        mailing (models.ForeignKey): Связь с моделью `Mailing`, обязательное поле. При удалении рассылки удаляются
                                     связанные попытки отправки.
        time (models.DateTimeField): Дата и время попытки отправки, автоматически устанавливаемое поле.
        status (models.CharField): Статус попытки отправки, обязательное поле, максимальная длина 10 символов.
        log_message (models.TextField): Лог сообщения, дополнительное поле.
    """

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки отправки')
    status = models.CharField(max_length=10, choices=Mailing.STATUS_CHOICES, verbose_name='Статус попытки отправки')
    log_message = models.TextField(verbose_name='Лог сообщения', **NULLABLE)

    def __str__(self):
        return f'Попытка отправки рассылки {self.mailing.title} на {self.time}'

    def get_mailing_owner(self):
        return self.mailing.owner

    class Meta:
        verbose_name = 'Попытка отправки рассылки'
        verbose_name_plural = 'Попытки отправки рассылок'
