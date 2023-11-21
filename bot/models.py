# botapp/models.py
from django.db import models
from django.contrib.auth.models import User

class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_document = models.ImageField(upload_to='id_documents/', null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)

    def __str__(self):
        return self.user.username