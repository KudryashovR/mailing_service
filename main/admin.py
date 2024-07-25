from django.contrib import admin

from main.models import Mailing, Client, MailingAttempt, BlogPost


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'status', 'scheduled_time', 'periodicity')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'get_initials')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'time','status', 'log_message')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'view_count')
    search_fields = ('title', 'content')
