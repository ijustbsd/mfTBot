#!/usr/bin/env python3
# -*-coding: utf-8-*-
import json
from time import sleep

import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardRemove
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id
)

from libs.users import add_user, load_user
from libs.stats import update_stats, load_stats
from libs.schedule import (
    today_schedule, week_schedule, bells_schedule, gr_to_dir, schedule_title,
    days_schedule
)
from answers import *
from inline_btns import course_btns, group_btns
import config


def listmerge(lst):
    merge_lists = []
    for l in lst:
        for item in l:
            merge_lists.append(item)
    return merge_lists

records = telepot.helper.SafeDict()


class MathBot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MathBot, self).__init__(*args, **kwargs)

        with open('data/keyboards.json') as json_file:
            keyboards = json.load(json_file)
        self.keyboard = keyboards["keyboard"]
        self.week_keyboard = keyboards["week_keyboard"]
        self.other_keyboard = keyboards["other_keyboard"]

        global records
        if self.id in records:
            self.count, self.edit_msg_ident = records[self.id]
            if self.edit_msg_ident:
                self.editor = telepot.helper.Editor(
                    self.bot,
                    self.edit_msg_ident
                )
            else:
                None
        else:
            self.count = 0
            self.edit_msg_ident = None
            self.editor = None

    def registration(self, user_id, course=None, group=None):
        if course:
            self.cancel_last()
            self.sender.sendMessage(course)
            add_user(user_id, course, "")
            sent = self.sender.sendMessage(
                reg_msg_2,
                reply_markup=group_btns[int(course) - 1]
            )
            self.editor = telepot.helper.Editor(self.bot, sent)
            self.edit_msg_ident = telepot.message_identifier(sent)
        elif group:
            course = load_user(user_id)[0]["course"]
            self.cancel_last()
            if int(course) > 2:
                self.sender.sendMessage(gr_to_dir(group))
            else:
                self.sender.sendMessage('.'.join(group))
            add_user(user_id, course, group)
            self.sender.sendMessage(reg_msg_3, reply_markup=self.keyboard)
            self.close()
        else:
            sent = self.sender.sendMessage(reg_msg_1, reply_markup=course_btns)
            self.editor = telepot.helper.Editor(self.bot, sent)
            self.edit_msg_ident = telepot.message_identifier(sent)

    def answerer(self, user_id, cmd):
        if cmd == '/start':
            if not load_user(user_id):
                self.sender.sendMessage(
                    reg_msg_0,
                    reply_markup=ReplyKeyboardRemove()
                )
                self.registration(user_id)
                update_stats(new_user=1)
            else:
                self.sender.sendMessage(start_msg, reply_markup=self.keyboard)
        elif cmd == self.keyboard['keyboard'][0][0]:
            titles = schedule_title(user_id)
            for s, t in zip(today_schedule(user_id), titles):
                self.sender.sendMessage(
                    '*Расписание на сегодня:\n(%s)*\n%s' % (t, s),
                    'Markdown',
                    reply_markup=self.keyboard
                )
            update_stats(new_msg=1)
        elif cmd == self.keyboard['keyboard'][0][1]:
            titles = schedule_title(user_id)
            for s, t in zip(today_schedule(user_id, 1), titles):
                self.sender.sendMessage(
                    '*Расписание на завтра:\n(%s)*\n%s' % (t, s),
                    'Markdown',
                    reply_markup=self.keyboard
                )
            update_stats(new_msg=1)
        elif cmd == self.keyboard['keyboard'][1][0]:
            self.sender.sendMessage(
                'Выберите день недели:',
                reply_markup=self.week_keyboard
            )
        elif cmd in listmerge(self.week_keyboard['keyboard']):
            index = listmerge(self.week_keyboard['keyboard']).index(cmd)
            titles = schedule_title(user_id)
            output = days_schedule[index] + '\n'
            for s, t in zip(week_schedule(user_id, index), titles):
                output += '*%s*\n%s\n\n' % (t, s)
            self.sender.sendMessage(
                output,
                'Markdown',
                reply_markup=self.keyboard
            )
            update_stats(new_msg=1)
        elif cmd == self.keyboard['keyboard'][2][0]:
            self.sender.sendMessage(
                bells_schedule,
                'Markdown',
                reply_markup=self.keyboard
            )
            update_stats(new_msg=1)
        elif cmd == self.keyboard['keyboard'][3][0]:
            self.sender.sendMessage(
                settings_msg,
                'Markdown',
                reply_markup=self.other_keyboard
            )
        elif cmd == self.other_keyboard['keyboard'][0][0]:
            self.sender.sendMessage(
                again_msg,
                reply_markup=ReplyKeyboardRemove()
            )
            self.registration(user_id)
        elif cmd == self.other_keyboard['keyboard'][1][0]:
            self.sender.sendMessage(
                updates_msg,
                'Markdown',
                reply_markup=self.keyboard
            )
        elif cmd == self.other_keyboard['keyboard'][2][0]:
            self.sender.sendMessage(
                feedback_msg,
                'Markdown',
                reply_markup=self.keyboard
            )
        elif cmd == self.other_keyboard['keyboard'][3][0]:
            self.sender.sendMessage(
                back_button_msg,
                'Markdown',
                reply_markup=self.keyboard
            )
        elif cmd == '/stats' and str(user_id) in config.admins:
            users, messages = load_stats()
            self.sender.sendMessage(
                '*Статистика:*\nПользователей: %d\nСообщений: %d' % (
                    users, messages),
                'Markdown',
                reply_markup=self.keyboard
            )
        else:
            self.sender.sendMessage(error_msg, reply_markup=self.keyboard)

    def cancel_last(self):
        if self.editor:
            self.editor.editMessageReplyMarkup(reply_markup=None)
            self.editor = None
            self.edit_msg_ident = None

    def on_chat_message(self, msg):
        content_type = telepot.glance(msg)[0]
        user_id = telepot.glance(msg)[2]
        if content_type == 'text':
            self.answerer(user_id, msg['text'])
        else:
            self.sender.sendMessage(error_msg, reply_markup=self.keyboard)

    def on_callback_query(self, msg):
        query, from_id, data = telepot.glance(msg, flavor='callback_query')
        groups = ('11', '12', '21', '31', '32', '33', '41', '42', '51', '52')
        if int(data) in range(1, 6):
            self.registration(from_id, course=data)
        elif data in groups:
            self.registration(from_id, group=data)

    def on_close(self, ex):
        global records
        records[self.id] = (self.count, self.edit_msg_ident)

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
