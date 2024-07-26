from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Менеджер')

        permissions = [
            Permission.objects.get(codename='view_blogpost'),
            Permission.objects.get(codename='view_mailing'),
            Permission.objects.get(codename='view_user'),
            Permission.objects.get(codename='set_active'),
            Permission.objects.get(codename='set_status_disregard'),
        ]

        for perm in permissions:
            group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Создана/обновлена группа Менеджер'))