#!/usr/bin/env python3
# -*-coding: utf-8-*-
import json
from time import sleep

import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import (
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

from libs.users import load_user, add_schedule, del_schedule
from libs.stats import new_user, new_msg
from libs.schedule import gr_to_dir, schedule_title
from answers import Answers as answ
from inline_btns import qual_btns, course_btns, group_btns
from config import TOKEN


def listmerge(lst):
    merge_lists = []
    for l in lst:
        for item in l:
            merge_lists.append(item)
    return merge_lists


def qual_to_word(qual):
    titles = {
        "spo": "СПО",
        "bach": "Бакалавр"
    }
    return titles[qual]


def del_keyboard_gen(chatid):
    titles = schedule_title(chatid)
    btns = []
    for s in titles:
        callback = 'del_%d' % (titles.index(s))
        btns.append([
            InlineKeyboardButton(text=s, callback_data=callback)
            ])
    return InlineKeyboardMarkup(inline_keyboard=btns)

records = telepot.helper.SafeDict()


class MathBot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MathBot, self).__init__(*args, **kwargs)

        with open('data/keyboards.json') as json_file:
            keyboards = json.load(json_file)
        self.keyboard = keyboards["keyboard"]
        self.week_keyboard = keyboards["week_keyboard"]
        self.other_keyboard = keyboards["other_keyboard"]
        self.add_del_keyboard = keyboards["add_del_keyboard"]

        global records
        if self.id in records:
            self.count, self.edit_msg_ident, self.users = records[self.id]
            if self.edit_msg_ident:
                self.editor = telepot.helper.Editor(
                    self.bot,
                    self.edit_msg_ident
                )
            else:
                self.editor = None
        else:
            self.count = 0
            self.edit_msg_ident = None
            self.editor = None
            self.users = {}

        self.commands = {
            '/start': self.startcmd,
            self.keyboard['keyboard'][0][0]: self.todaycmd,
            self.keyboard['keyboard'][0][1]: self.tomorrowcmd,
            self.keyboard['keyboard'][1][0]: self.weekcmd,
            self.keyboard['keyboard'][2][0]: self.bellscmd,
            self.keyboard['keyboard'][3][0]: self.settingscmd,
            self.other_keyboard['keyboard'][0][0]: self.add_del_cmd,
            self.other_keyboard['keyboard'][1][0]: self.distrcmd,
            self.other_keyboard['keyboard'][2][0]: self.feedbackcmd,
            self.other_keyboard['keyboard'][2][1]: self.updatecmd,
            self.other_keyboard['keyboard'][3][0]: self.backcmd,
            self.add_del_keyboard['keyboard'][0][0]: self.add_schd_cmd,
            self.add_del_keyboard['keyboard'][1][0]: self.del_schd_cmd,
            self.add_del_keyboard['keyboard'][2][0]: self.changecmd
        }
        weekkeys = listmerge(self.week_keyboard['keyboard'])
        for k in weekkeys:
            self.commands[k] = self.weekschd

    def registration(self, chatid, qual=None, course=None, group=None):
        if qual:
            self.cancel_last()
            self.users[chatid]["qual"] = qual
            self.sender.sendMessage(qual_to_word(qual))
            sent = self.sender.sendMessage(
                answ.reg_2,
                reply_markup=course_btns[self.users[chatid]["qual"]]
            )
            self.editor = telepot.helper.Editor(self.bot, sent)
            self.edit_msg_ident = telepot.message_identifier(sent)
        elif course:
            self.cancel_last()
            self.users[chatid]["course"] = course
            self.sender.sendMessage(course)
            q = self.users[chatid]["qual"]
            sent = self.sender.sendMessage(
                answ.reg_3,
                reply_markup=group_btns[q][int(course) - 1]
            )
            self.editor = telepot.helper.Editor(self.bot, sent)
            self.edit_msg_ident = telepot.message_identifier(sent)
        elif group:
            self.cancel_last()
            self.users[chatid]["group"] = group
            if self.users[chatid]["qual"] == "spo":
                self.sender.sendMessage(gr_to_dir("spo", group))
            else:
                if int(self.users[chatid]["course"]) > 2:
                    self.sender.sendMessage(gr_to_dir("bach", group))
                else:
                    self.sender.sendMessage('.'.join(group))
            user = self.users[chatid]
            add_schedule(chatid, user["qual"], user["course"], user["group"])
            self.sender.sendMessage(answ.reg_4, reply_markup=self.keyboard)
            self.close()
        else:
            self.users[chatid] = {
                "qual": "bach",
                "course": "1",
                "group": "41"
            }
            sent = self.sender.sendMessage(answ.reg_1, reply_markup=qual_btns)
            self.editor = telepot.helper.Editor(self.bot, sent)
            self.edit_msg_ident = telepot.message_identifier(sent)

    def startcmd(self, chatid, *kwargs):
        if not load_user(chatid):
            self.sender.sendMessage(
                answ.reg_0,
                reply_markup=ReplyKeyboardRemove())
            self.registration(chatid)
        else:
            self.sender.sendMessage(answ.start, reply_markup=self.keyboard)

    def todaycmd(self, chatid, *kwargs):
        messages = answ(chatid).today_msg()
        for msg in messages:
            self.sender.sendMessage(msg, 'Markdown', reply_markup=self.keyboard)

    def tomorrowcmd(self, chatid, *kwargs):
        messages = answ(chatid).today_msg(1)
        for msg in messages:
            self.sender.sendMessage(msg, 'Markdown', reply_markup=self.keyboard)

    def weekcmd(self, *kwargs):
        self.sender.sendMessage(answ.weekday, reply_markup=self.week_keyboard)

    def weekschd(self, chatid, cmd):
        index = listmerge(self.week_keyboard['keyboard']).index(cmd)
        msg = answ(chatid).week_msg(index)
        self.sender.sendMessage(msg, 'Markdown', reply_markup=self.keyboard)

    def bellscmd(self, *kwargs):
        self.sender.sendMessage(
            answ.bells,
            'Markdown',
            reply_markup=self.keyboard)

    def settingscmd(self, *kwargs):
        self.sender.sendMessage(
            answ.settings,
            'Markdown',
            reply_markup=self.other_keyboard)

    def add_del_cmd(self, *kwargs):
        self.sender.sendMessage(
            'Выберите действие:',
            reply_markup=self.add_del_keyboard)

    def distrcmd(self, *kwargs):
        self.sender.sendMessage(
            "Функция в разработке \U0001F527",
            'Markdown',
            reply_markup=self.keyboard)

    def feedbackcmd(self, *kwargs):
        self.sender.sendMessage(
            answ.feedback,
            'Markdown',
            reply_markup=self.keyboard)

    def updatecmd(self, *kwargs):
        self.sender.sendMessage(
            answ.updates,
            'Markdown',
            reply_markup=self.keyboard)

    def backcmd(self, *kwargs):
        self.sender.sendMessage(
            answ.back_button,
            'Markdown',
            reply_markup=self.keyboard)

    def add_schd_cmd(self, chatid, *kwargs):
        self.sender.sendMessage(
            'Какое расписание нужно добавить?',
            'Markdown',
            reply_markup=ReplyKeyboardRemove())
        self.registration(chatid)

    def del_schd_cmd(self, chatid, *kwargs):
        sent = self.sender.sendMessage(
            'Какое расписание нужно убрать?',
            'Markdown',
            reply_markup=del_keyboard_gen(chatid))
        self.editor = telepot.helper.Editor(self.bot, sent)
        self.edit_msg_ident = telepot.message_identifier(sent)

    def changecmd(self, *kwargs):
        self.distrcmd()

    def errorcmd(self, *kwargs):
        self.sender.sendMessage(answ.error, reply_markup=self.keyboard)

    def answerer(self, chatid, cmd):
        answer = self.commands.get(cmd, self.errorcmd)
        answer(chatid, cmd)

    def cancel_last(self):
        if self.editor:
            self.editor.editMessageReplyMarkup(reply_markup=None)
            self.editor = None
            self.edit_msg_ident = None

    def on_chat_message(self, msg):
        content_type = telepot.glance(msg)[0]
        chatid = telepot.glance(msg)[2]
        if content_type == 'text':
            self.answerer(chatid, msg['text'])
            new_msg(chatid, msg['text'])
            userdata = msg['from']
            firstname = userdata.get('first_name')
            lastname = userdata.get('last_name')
            username = userdata.get('username')
            new_user(chatid, firstname, lastname, username)
        else:
            self.sender.sendMessage(answ.error, reply_markup=self.keyboard)

    def on_callback_query(self, msg):
        _query, from_id, data = telepot.glance(msg, flavor='callback_query')
        spo_gr = ('11', '12', '21', '22')
        bach_gr = ('11', '12', '21', '31', '32', '33', '41', '42', '51', '52')
        if data in ["spo", "bach", "master", "add_edu"]:
            self.registration(from_id, qual=data)
        elif "del" in data:
            self.cancel_last()
            titles = schedule_title(from_id)
            self.sender.sendMessage(titles[int(data[4:])], reply_markup=self.keyboard)
            del_msg = del_schedule(from_id, data[4:])
            self.sender.sendMessage(del_msg, reply_markup=self.keyboard)
        elif int(data) in range(1, 6):
            self.registration(from_id, course=data)
        elif data in spo_gr or bach_gr:
            self.registration(from_id, group=data)

    def on_close(self, ex):
        global records
        records[self.id] = (self.count, self.edit_msg_ident, self.users)

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']),
            create_open,
            MathBot,
            timeout=10
        )
    ])

MessageLoop(bot).run_as_thread()

while 1:
    sleep(10)
