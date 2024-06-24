from django.contrib import admin

from main.models import Mailing, Client


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'status', 'scheduled_time')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name', 'second_name', 'comment')

