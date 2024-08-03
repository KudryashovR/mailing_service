from django.core.cache import cache
from django.db import models

from config import settings
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
        owner (models.ForeignKey): Владелец клиента, связь с моделью пользователя (User), обязательное поле.

    Методы:
        get_full_name(): Возвращает полное имя клиента.
        get_initials(): Возвращает инициалы клиента.
        get_client_owner(): Возвращает владельца клиента.
        get_unique_clients(): Статический метод, возвращает количество уникальных клиентов.
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
        """
        Возвращает владельца клиента.

        Возвращает:
            User: Экземпляр пользователя, являющийся владельцем клиента.
        """

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

    @staticmethod
    def get_unique_clients():
        """
        Статический метод, возвращает количество уникальных клиентов.

        Возвращает:
            int: Количество уникальных клиентов.
        """

        unique_clients = Client.objects.count()

        if settings.CACHE_ENABLED:
            key = 'unique_clients'
            cache_data = cache.get(key)

            if cache_data is None:
                cache_data = unique_clients
                cache.set(key, cache_data, timeout=60)

            return cache_data

        return unique_clients


class Mailing(models.Model):
    """
    Модель представляет рассылку.

    Перечисления:
        STATUS_CHOICES (list): Список возможных статусов рассылки.
        PERIODICITY_CHOICES (list): Список возможных периодичностей рассылки.

    **Атрибуты:**
        title (models.CharField): Заголовок рассылки, обязательное поле, максимальная длина 255 символов.
        message (models.TextField): Содержание рассылки, обязательное поле.
        status (models.CharField): Статус рассылки, обязательное поле, максимальная длина 10 символов, по умолчанию 'Новый'.
        scheduled_time (models.DateTimeField): Дата и время отправки рассылки, обязательное поле.
        periodicity (models.CharField): Периодичность рассылки, обязательное поле, максимальная длина 15 символов, по умолчанию 'Ежедневно'.
        clients (models.ManyToManyField): Список клиентов, которым будет отправлена рассылка.
        owner (models.ForeignKey): Владелец рассылки, связь с моделью пользователя (User), обязательное поле.

    Методы:
        __str__(): Возвращает заголовок рассылки.
        set_status_disregard(): Устанавливает статус рассылки 'Отклонен' и сохраняет изменения.
        get_total_mailings(): Статический метод, возвращает общее количество рассылок.
        get_active_mailings(): Статический метод, возвращает количество активных рассылок.
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

        permissions = [
            (
                'set_status_disregard',
                'Отключение рассылки.'
            )
        ]

    @staticmethod
    def get_total_mailings():
        """
        Возвращает общее количество рассылок.

        Если включено кеширование, данные будут получены из кеша или сохранены в кеш при отсутствии.

        Возвращает:
            int: Общее количество рассылок.
        """

        if settings.CACHE_ENABLED:
            key = 'total_mailings'
            cache_data = cache.get(key)

            if cache_data is None:
                total_mailings = Mailing.objects.count()
                cache_data = total_mailings
                cache.set(key, cache_data, timeout=60)

            return cache_data

        return Mailing.objects.count()

    @staticmethod
    def get_active_mailings():
        """
        Возвращает количество активных рассылок.

        Если включено кеширование, данные будут получены из кеша или сохранены в кеш при отсутствии.

        Возвращает:
            int: Количество активных рассылок.
        """

        if settings.CACHE_ENABLED:
            key = 'active_mailings'
            cache_data = cache.get(key)

            if cache_data is None:
                active_mailings = Mailing.objects.filter(status='Новый').count() + Mailing.objects.filter(
                    status='Отправлен').count()
                cache_data = active_mailings
                cache.set(key, cache_data, timeout=60)

            return cache_data

        return Mailing.objects.filter(status='Новый').count() + Mailing.objects.filter(status='Отправлен').count()

    def set_status_disregard(self):
        """
        Устанавливает статус рассылки 'Отклонен' и сохраняет изменения.
        """

        self.status = 'Отклонен'
        self.save()


class MailingAttempt(models.Model):
    """
    Модель представляет попытку отправки рассылки.

    Атрибуты:
        mailing (models.ForeignKey): Ссылка на модель Mailing, обязательное поле. При удалении рассылки
                                     удаляются и связанные с ней попытки отправки.
        time (models.DateTimeField): Дата и время попытки отправки, устанавливается автоматически при создании.
        status (models.CharField): Статус попытки отправки, обязательное поле, максимальная длина 10 символов.
        log_message (models.TextField): Лог сообщения, дополнительное поле с возможностью быть пустым.
    """

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки отправки')
    status = models.CharField(max_length=10, choices=Mailing.STATUS_CHOICES, verbose_name='Статус попытки отправки')
    log_message = models.TextField(verbose_name='Лог сообщения', **NULLABLE)

    def __str__(self):
        """
        Строковое представление объекта MailingAttempt, возвращает информацию о попытке отправки.

        Возвращает:
            str: Информация о попытке отправки рассылки с датой и временем отправки.
        """

        return f'Попытка отправки рассылки {self.mailing.title} на {self.time}'

    def get_mailing_owner(self):
        """
        Возвращает владельца рассылки, к которой относится данная попытка отправки.

        Возвращает:
            User: Владелец рассылки.
        """

        return self.mailing.owner

    class Meta:
        verbose_name = 'Попытка отправки рассылки'
        verbose_name_plural = 'Попытки отправки рассылок'


class BlogPost(models.Model):
    """
    Модель представляет статью блога.

    Атрибуты:
        title (models.CharField): Наименование статьи, обязательное поле, максимальная длина 200 символов.
        content (models.TextField): Содержание статьи, текстовое поле.
        image (models.ImageField): Изображение, дополнительное поле. Поддерживает загрузку изображений
                                   в каталог 'blog_images'. Поле может быть пустым и необязательным.
        view_count (models.PositiveIntegerField): Количество просмотров статьи, поле с положительным числовым значением.
        published_date (models.DateTimeField): Дата и время публикации статьи, автоматически устанавливается
                                                    при создании.
    """

    title = models.CharField(max_length=200, verbose_name='Наименование статьи')
    content = models.TextField(verbose_name='Содержание статьи')
    image = models.ImageField(upload_to='blog_images', **NULLABLE, verbose_name='Изображение')
    view_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Строковое представление объекта BlogPost, возвращает заголовок статьи.

        Возвращает:
            str: Заголовок статьи.
        """

        return self.title

    class Meta:
        verbose_name = 'Статья блога'
        verbose_name_plural = 'Статьи блога'

    @staticmethod
    def get_ramdom_articles(count):
        """
        Возвращает список случайных статей блога.

        Параметры:
            count (int): Количество случайных статей для возврата.

        Возвращает:
            QuerySet: Набор случайных статей блога.

        Примечание:
            Если в настройках включено кеширование, данные будут извлекаться из кеша с ключом 'articles'. Кэш
            обновляется каждые 60 секунд.
        """

        if settings.CACHE_ENABLED:
            key = 'articles'
            cache_data = cache.get(key)

            if cache_data is None:
                articles = BlogPost.objects.order_by('?')
                cache_data = articles
                cache.set(key, cache_data, timeout=60)

            return cache_data[:count]

        return BlogPost.objects.order_by('?')[:count]
