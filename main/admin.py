from django.contrib import admin

from main.models import Mailing, Client, MailingAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'status', 'scheduled_time')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'get_initials')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'time','status')
