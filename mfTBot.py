# -*-coding: utf-8-*-
from time import sleep
import datetime
import json
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id
)

from answers import *
import config


def listmerge(lst):
    merge_lists = []
    for l in lst:
        for item in l:
            merge_lists.append(item)
    return merge_lists


class MathBot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MathBot, self).__init__(*args, **kwargs)

        with open('data/keyboards.json') as json_file:
            keyboards = json.load(json_file)
        self.keyboard = keyboards["keyboard"]
        self.week_keyboard = keyboards["week_keyboard"]

        with open('data/timetables/3.json') as json_file:
            timetable = json.load(json_file)
        self.num_sch = ['\n'.join(i) for i in timetable["numerator"]]
        self.denom_sch = ['\n'.join(i) for i in timetable["denominator"]]

    def answerer(self, user_id, cmd):
        if cmd == '/start':
            self.sender.sendMessage(start_msg, reply_markup=keyboard)
        elif cmd == self.keyboard['keyboard'][0][0]:
            today = datetime.date.today()
            weekday = today.weekday()
            is_num = today.isocalendar()[1] % 2
            rasp = self.num_sch[weekday] if is_num else self.denom_sch[weekday]
            self.sender.sendMessage(
                '*Расписание на сегодня:*\n' + rasp,
                'Markdown'
            )
        elif cmd == self.keyboard['keyboard'][1][0]:
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            weekday = tomorrow.weekday()
            is_num = tomorrow.isocalendar()[1] % 2
            rasp = self.num_sch[weekday] if is_num else self.denom_sch[weekday]
            self.sender.sendMessage(
                '*Расписание на завтра:*\n' + rasp,
                'Markdown'
            )
        elif cmd == self.keyboard['keyboard'][2][0]:
            self.sender.sendMessage(
                'Выберите день недели:',
                reply_markup=self.week_keyboard
            )
        elif cmd in listmerge(self.week_keyboard['keyboard']):
            index = listmerge(self.week_keyboard['keyboard']).index(cmd)
            if self.num_sch[index] == self.denom_sch[index]:
                self.sender.sendMessage(
                    days_schedule[index] + self.num_sch[index],
                    'Markdown',
                    reply_markup=self.keyboard
                )
            else:
                self.sender.sendMessage(
                    '%s*Числитель:*\n%s\n*Знаменатель:*\n%s' % (
                        days_schedule[index],
                        self.num_sch[index],
                        self.denom_sch[index]
                    ),
                    'Markdown',
                    reply_markup=self.keyboard
                )
        elif cmd == self.keyboard['keyboard'][3][0]:
            self.sender.sendMessage(
                bells_schedule,
                'Markdown',
                reply_markup=self.keyboard
            )
        else:
            self.sender.sendMessage(error_msg)

    def on_chat_message(self, msg):
        content_type = telepot.glance(msg)[0]
        user_id = telepot.glance(msg)[2]
        if content_type == 'text':
            self.answerer(user_id, msg['text'])
        else:
            self.sender.sendMessage(error_msg)

bot = telepot.DelegatorBot(config.TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']),
            create_open,
            MathBot,
            timeout=10
        )
    ]
)
MessageLoop(bot).run_as_thread()

while 1:
    sleep(10)
