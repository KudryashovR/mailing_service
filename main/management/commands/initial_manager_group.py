from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Менеджер')

        permissions = [
            Permission.objects.get(codename='can_add_blogpost'),
            Permission.objects.get(codename='can_change_blogpost'),
            Permission.objects.get(codename='can_delete_blogpost'),
            Permission.objects.get(codename='can_view_blogpost'),
            Permission.objects.get(codename='can_view_mailing'),
            Permission.objects.get(codename='can_change_user'),
            Permission.objects.get(codename='can_view_user'),
        ]

        for perm in permissions:
            group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Создана группа Менеджер'))