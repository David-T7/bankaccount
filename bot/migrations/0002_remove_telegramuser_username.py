# Generated by Django 4.2.7 on 2023-11-21 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='username',
        ),
    ]
