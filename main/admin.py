from django.contrib import admin

from main.models import Mailing, Client, MailingAttempt, BlogPost


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для управления моделью Mailing.

    Отображает следующие поля в списке:
    - title (Заголовок)
    - message (Сообщение)
    - status (Статус)
    - scheduled_time (Запланированное время)
    - periodicity (Периодичность)
    """

    list_display = ('title', 'message', 'status', 'scheduled_time', 'periodicity')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для управления моделью Client.

    Отображает следующие поля в списке:
    - email (Email)
    - get_initials (Инициалы)
    """

    list_display = ('email', 'get_initials')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для управления моделью MailingAttempt.

    Отображает следующие поля в списке:
    - mailing (Рассылка)
    - time (Время)
    - status (Статус)
    - log_message (Лог сообщения)
    """

    list_display = ('mailing', 'time','status', 'log_message')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для управления моделью BlogPost.

    Отображает следующие поля в списке:
    - title (Заголовок)
    - published_date (Дата публикации)
    - view_count (Количество просмотров)

    Включает поля для поиска:
    - title (Заголовок)
    - content (Содержание)
    """

    list_display = ('title', 'published_date', 'view_count')
    search_fields = ('title', 'content')
