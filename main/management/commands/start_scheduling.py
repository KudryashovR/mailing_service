from django.core.management.base import BaseCommand
from ...tasks import start


class Command(BaseCommand):
    help = 'Start the mailing scheduler'

    def handle(self, *args, **kwargs):
        start()
