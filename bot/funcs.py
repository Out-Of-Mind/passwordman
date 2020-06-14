from telebot import TeleBot
from .models import TelegramUser, SitePassword
import time, os

def parse(r):
	bot = TeleBot(os.getenv('TELE_TOKEN'))
	chat_id = r['message']['chat']['id']
	message = r['message']['text']
	try:
		user = TelegramUser.objects.get(chat_id=chat_id)
		if user.state:
			passw = message
			if user.password == passw:
				bot.send_message(chat_id, 'пароль принят!!!')
				user.last_login = int(time.time())
				user.state = False
				user.save()
				return True
			else:
				bot.send_message(chat_id, 'пароль неверен((((')
				return False
		u = True
		t1 = time.time()
		t = t1 - user.last_login
		t2 = int(time.ctime(t)[14:16])
		if t2 > 5:
			user.state = True
			user.save()
			bot.send_message(chat_id, 'Чтобы получить доступ к функционалу надо ввести мастер пароль! Просто отправьте мне его сообщением')
			return False
	except Exception as e:
		user = TelegramUser.objects.create(chat_id=chat_id, last_login=int(time.time()))
		user.save()
		u = False
	if message == '/start':
		if u:
			bot.send_message(chat_id, 'Я тебя помню, где-то я уже видел тебя...')
			user.last_login = int(time.time())
			user.save()
		else:
			bot.send_message(chat_id, 'Привет, я создан для того чтобы хранить твои пароли! Сейчас просто отправь мне команду /set_password passw с твоим паролем для установки его как мастер пароль!!! \n(Его можно будет потом изменить) Установить мастер пароль это обязательно, потому что, через пять минут бездействия он будет затребован')
			user.last_login = int(time.time())
			user.save()
	elif '/set_password' in message:
		password = message[14:]
		user.password = password
		user.last_login = int(time.time())
		user.save()
		bot.send_message(chat_id, 'успешно установлен мастер пароль')
	elif message == '/get_all':
		passwords = SitePassword.objects.filter(tele_user=user)
		user.last_login = int(time.time())
		user.save()
		if len(passwords) == 0:
			bot.send_message(chat_id, 'Ты пока еще ничего не записал')
		else:
			for i in passwords:
				bot.send_message(chat_id, 'сайт: {}, логин {}, пароль: {}'.format(i.site, i.login, i.password))
	elif '/site' in message:
		user.last_login = int(time.time())
		user.save()
		try:
			site = SitePassword.objects.filter(site=message[6:])
			for s in site:
				bot.send_message(chat_id, 'уникальный айди: {}, сайт: {}, логин: {}, пароль: {}'.format(s.id, s.site, s.login, s.password))
		except:
			bot.send_message(chat_id, 'Не могу найти такую запись...(((')
	elif '/delete' in message:
		user.last_login = int(time.time())
		user.save()
		id = message[8:]
		try:
			site = SitePassword.objects.get(id=message[8:])
			bot.send_message(chat_id, 'Была успешно удалена запись с айди: {}'.format(id))
			SitePassword.objects.get(id=message[8:]).delete()
		except Exception as e:
			bot.send_message(chat_id, 'Записи с айди {} не существует!'.format(id))
	elif '/set' in message:
		user.last_login = int(time.time())
		message = message[5:]
		url = ''
		i = message.index(' ')
		url = message[:i]
		message = message[i+1:]
		i = message.index(' ')
		login = message[:i]
		message = message[i+1:]
		passw = message
		s = SitePassword.objects.create(tele_user=user, site=url, login=login, password=passw)
		user.save()
		bot.send_message(chat_id, 'Успешно создана запись с айди: {}'.format(s.id))
	elif message == '/help':
		user.last_login = int(time.time())
		user.save()
		bot.send_message(chat_id, 'Для того, чтобы установить или переустановить мастер пароль надо вести команду /set_password passw, где passw это пароль,\nдля того, чтобы просмотреть все записи надо ввести команду /get_all,\nдля того, чтобы просмотреть записи с определенного сайта надо ввести команду /site https://web-site.com, где https://web-site.com это ссылка на сайт,\nдля того, чтобы удалить запись надо ввести команду /delete id, где id это уникальный айди,\nдля того, чтобы создать нову запись надо ввести команду /set https://example.com login passw, где https://example.com это ссылка на сайт, login это логин от сайта и passw это пароль от сайта,\nдля того, чтобы удалить все данные о себе надо ввести команду /drop')
	elif message == '/drop':
		user.last_login = int(time.time())
		user.save()
		TelegramUser.objects.get(chat_id=chat_id).delete()
		bot.send_message(chat_id, 'удалены все данные о вас')
	else:
		user.last_login = int(time.time())
		user.save()
		bot.send_message(chat_id, 'такая команда не найдена(((, попробуй ввести /help')