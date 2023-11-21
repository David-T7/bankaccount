# botapp/models.py
from django.db import models

class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
