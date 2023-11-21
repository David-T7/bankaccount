from django.contrib import admin
from .models import TelegramUser , UserProfile
# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(UserProfile)