# Generated by Django 5.0.6 on 2024-06-24 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingattempt',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки отправки'),
        ),
    ]
