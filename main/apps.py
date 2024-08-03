from django.apps import AppConfig
from time import sleep


class MainConfig(AppConfig):
    """
    Конфигурация приложения 'main'.

    Атрибуты:
    default_auto_field (str): Тип поля по умолчанию для автоинкрементных полей.
    name (str): Имя приложения.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from .tasks import start
        sleep(2)
        start()
