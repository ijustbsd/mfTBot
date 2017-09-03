# -*-coding: utf-8-*-
from time import sleep
import datetime
import json
import telepot

from answers import *
import config


def listmerge(lst):
    merge_lists = []
    for l in lst:
        for item in l:
            merge_lists.append(item)
    return merge_lists


class MathBot(telepot.Bot):
    def __init__(self, token):
        super().__init__(token)

        with open('data/keyboards.json') as json_file:
            keyboards = json.load(json_file)
        self.keyboard = keyboards["keyboard"]
        self.week_keyboard = keyboards["week_keyboard"]

        with open('data/timetables/3.json') as json_file:
            timetable = json.load(json_file)
        self.num_sch = ['\n'.join(i) for i in timetable["numerator"]]
        self.denom_sch = ['\n'.join(i) for i in timetable["denominator"]]

    def answerer(self, chatId, cmd):
        if cmd == '/start':
            self.sendMessage(chatId, start_msg, reply_markup=self.keyboard)
        elif cmd == self.keyboard['keyboard'][0][0]:
            today = datetime.date.today()
            weekday = today.weekday()
            is_num = today.isocalendar()[1] % 2
            rasp = self.num_sch[weekday] if is_num else self.denom_sch[weekday]
            self.sendMessage(
                chatId,
                '*Расписание на сегодня:*\n' + rasp,
                'Markdown'
            )
        elif cmd == self.keyboard['keyboard'][1][0]:
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            weekday = tomorrow.weekday()
            is_num = tomorrow.isocalendar()[1] % 2
            rasp = self.num_sch[weekday] if is_num else self.denom_sch[weekday]
            self.sendMessage(
                chatId,
                '*Расписание на завтра:*\n' + rasp,
                'Markdown'
            )
        elif cmd == self.keyboard['keyboard'][2][0]:
            self.sendMessage(
                chatId,
                'Выберите день недели:',
                reply_markup=self.week_keyboard
            )
        elif cmd in listmerge(self.week_keyboard['keyboard']):
            index = listmerge(self.week_keyboard['keyboard']).index(cmd)
            if self.num_sch[index] == self.denom_sch[index]:
                self.sendMessage(
                    chatId,
                    days_schedule[index] + self.num_sch[index],
                    'Markdown',
                    reply_markup=self.keyboard
                )
            else:
                self.sendMessage(
                    chatId,
                    '%s*Числитель:*\n%s\n*Знаменатель:*\n%s' % (
                        days_schedule[index],
                        self.num_sch[index],
                        self.denom_sch[index]
                    ),
                    'Markdown',
                    reply_markup=self.keyboard
                )
        elif cmd == self.keyboard['keyboard'][3][0]:
            self.sendMessage(
                chatId,
                bells_schedule,
                'Markdown',
                reply_markup=self.keyboard
            )
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
