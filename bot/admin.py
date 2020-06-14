from django.contrib import admin
from .models import TelegramUser, SitePassword

admin.site.register(TelegramUser)
admin.site.register(SitePassword)