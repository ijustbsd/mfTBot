# -*-coding: utf-8-*-
from sys import argv
from time import sleep
import datetime
import telepot

class MathBot(telepot.Bot):
	def __init__(self, token):
		super().__init__(token)
		self.keyboard = {'keyboard': [['\U0001f4d8 Расписание на сегодня'], ['\U0001f4d7 Расписание на завтра'], ['\U0001f4c5 Расписание на другие дни'], ['\U0001f514 Расписание звонков']]}
		self.weekKeyboard = {'keyboard': [['Пн', 'Вт', 'Ср', 'Чт', 'Пт'], ['Суббота'], ['Воскресенье']]}
		def getRasp(path1, path2):
			f1 = open(path1, 'r', encoding = 'utf-8')
			f2 = open(path2, 'r', encoding = 'utf-8')
			return (f1.read().split('#\n'), f2.read().split('#\n'))
		self.raspChisl, self.raspZnam = getRasp('timetables/raspChisl.txt', 'timetables/raspZnam.txt')
		self.raspToDayTxt = (
			'*Расписание на понедельник:*\n',
			'*Расписание на вторник:*\n',
			'*Расписание на среду:*\n',
			'*Расписание на четверг:*\n',
			'*Расписание на пятницу:*\n',
			'*Расписание на субботу:*\n',
			'*Расписание на воскресенье:*\n'
		)
		self.raspZvon ='*Расписание звонков:*\n1. 8:00 - 9:35\n2. 9:45 - 11:20\n3. 11:30 - 13:05\n4. 13:25 - 15:00\n5. 15:10 - 16:45'

	def answerer(self, chatId, cmd):
		if cmd == '/start':
			self.sendMessage(chatId, 'Привет! Я помогу тебе узнать расписание, обращайся \U0001f609', reply_markup = self.keyboard)
		elif cmd == self.keyboard['keyboard'][0][0]:
			today = datetime.date.today()
			weekday = today.weekday()
			rasp = self.raspChisl[weekday] if today.isocalendar()[1] % 2 else self.raspZnam[weekday]
			self.sendMessage(chatId, '*Расписание на сегодня:*\n' + rasp , 'Markdown')
		elif cmd == self.keyboard['keyboard'][1][0]:
			tomorrow = datetime.date.today() + datetime.timedelta(days = 1)
			weekday = tomorrow.weekday()
			rasp = self.raspChisl[weekday] if tomorrow.isocalendar()[1] % 2 else self.raspZnam[weekday]
			self.sendMessage(chatId, '*Расписание на завтра:*\n' + rasp , 'Markdown')
		elif cmd == self.keyboard['keyboard'][2][0]:
			self.sendMessage(chatId, 'Выберите день недели:' , reply_markup = self.weekKeyboard)
		elif cmd in ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суббота', 'Воскресенье'):
			index = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суббота', 'Воскресенье').index(cmd)
			if self.raspChisl[index] == self.raspZnam[index]:
				self.sendMessage(chatId, self.raspToDayTxt[index] + self.raspChisl[index], 'Markdown', reply_markup = self.keyboard)
			else:
				self.sendMessage(chatId, self.raspToDayTxt[index] + '*Числитель:*\n' + self.raspChisl[index] + '\n*Знаменатель:*\n' + self.raspZnam[index], 'Markdown', reply_markup = self.keyboard)
		elif cmd == self.keyboard['keyboard'][3][0]:
			self.sendMessage(chatId, self.raspZvon , 'Markdown', reply_markup = self.keyboard)
		else:
			self.sendMessage(chatId, 'К сожалению, я тебя не понимаю \U0001f622')

	def listener(self, msg):
		contentType, *args, chatId = telepot.glance(msg)
		if contentType == 'text':
			self.answerer(chatId, msg['text'])
		else:
			self.sendMessage(chatId, 'К сожалению, я тебя не понимаю \U0001f622')

bot = MathBot(argv[1])
bot.message_loop(bot.listener)
while 1:
	sleep(10)