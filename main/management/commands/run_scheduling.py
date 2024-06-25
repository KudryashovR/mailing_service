from django.core.management import BaseCommand
from ...tasks import send_mailing


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        send_mailing()
