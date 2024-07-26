from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Контент-менеджер')

        permissions = [
            Permission.objects.get(codename='view_blogpost'),
            Permission.objects.get(codename='add_blogpost'),
            Permission.objects.get(codename='change_blogpost'),
            Permission.objects.get(codename='delete_blogpost'),
        ]

        for perm in permissions:
            group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Создана/обновлена группа Контент-менеджера'))