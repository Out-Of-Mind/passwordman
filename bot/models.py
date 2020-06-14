from django.db import models
import time

class TelegramUser(models.Model):
	chat_id = models.IntegerField()
	last_login = models.IntegerField()
	password = models.CharField(max_length=200)
	state = models.BooleanField(default=False)

class SitePassword(models.Model):
	id = models.AutoField(primary_key=True)
	tele_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
	site = models.TextField()
	login = models.CharField(max_length=100)
	password = models.CharField(max_length=200)