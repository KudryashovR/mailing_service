from django.apps import AppConfig
from time import sleep


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from .tasks import start
        sleep(2)
        start()
