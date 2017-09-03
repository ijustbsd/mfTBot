# -*-coding: utf-8-*-
from time import sleep
import datetime
import json
import telepot

from answers import *
import config


class MathBot(telepot.Bot):
    def __init__(self, token):
        super().__init__(token)

        with open('data/keyboards.json') as json_file:
            keyboards = json.load(json_file)
        self.keyboard = keyboards["keyboard"]
        self.week_keyboard = keyboards["week_keyboard"]

        with open('data/timetables/3.json') as json_file:
            timetable = json.load(json_file)
        self.raspChisl = ['\n'.join(i) for i in timetable["numerator"]]
        self.raspZnam = ['\n'.join(i) for i in timetable["denominator"]]

    def answerer(self, chatId, cmd):
        if cmd == '/start':
            self.sendMessage(chatId, start_msg, reply_markup=self.keyboard)
        elif cmd == self.keyboard['keyboard'][0][0]:
            today = datetime.date.today()
            weekday = today.weekday()
            rasp = self.raspChisl[weekday] if today.isocalendar()[1] % 2 else self.raspZnam[weekday]
            self.sendMessage(chatId, '*Расписание на сегодня:*\n' + rasp, 'Markdown')
        elif cmd == self.keyboard['keyboard'][1][0]:
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            weekday = tomorrow.weekday()
            rasp = self.raspChisl[weekday] if tomorrow.isocalendar()[1] % 2 else self.raspZnam[weekday]
            self.sendMessage(chatId, '*Расписание на завтра:*\n' + rasp, 'Markdown')
        elif cmd == self.keyboard['keyboard'][2][0]:
            self.sendMessage(chatId, 'Выберите день недели:', reply_markup=self.week_keyboard)
        elif cmd in ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суббота', 'Воскресенье'):
            index = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суббота', 'Воскресенье').index(cmd)
            if self.raspChisl[index] == self.raspZnam[index]:
                self.sendMessage(chatId, days_schedule[index] + self.raspChisl[index], 'Markdown', reply_markup=self.keyboard)
            else:
                self.sendMessage(chatId, days_schedule[index] + '*Числитель:*\n' + self.raspChisl[index] + '\n*Знаменатель:*\n' + self.raspZnam[index], 'Markdown', reply_markup=self.keyboard)
        elif cmd == self.keyboard['keyboard'][3][0]:
            self.sendMessage(chatId, bells_schedule, 'Markdown', reply_markup=self.keyboard)
        else:
            self.sendMessage(chatId, error_msg)

    def listener(self, msg):
        contentType, *args, chatId = telepot.glance(msg)
        if contentType == 'text':
            self.answerer(chatId, msg['text'])
        else:
            self.sendMessage(chatId, error_msg)

bot = MathBot(config.TOKEN)
bot.message_loop(bot.listener)
while 1:
    sleep(10)
