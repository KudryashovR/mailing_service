# Generated by Django 5.0.6 on 2024-07-26 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_blogpost'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('set_status_disregard', 'Отключение рассылки.')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]