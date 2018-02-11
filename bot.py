# -*- coding: utf-8 -*-
'''
Main file. Run it for bot start working.
'''

import datetime
import logging
import ssl
import time

import telebot
from aiohttp import web

from libs.db import DBManager
from libs.safedict import SafeDict
from libs.keyboards import (
    MainKeyboard, WeekKeyboard, SettingsKeyboard, SetSchedKeyboard, RmKeyboard,
    QualKeyboard, CourseKeyboards, BachelorsGroups, SpoGroups, DeleteSchdKeyboard)
from libs.answers import Answers as answ
from config import TOKEN, USE_LONG_POLLING, URL, WH_PORT

logger = telebot.logger
telebot.logger.setLevel(logging.ERROR)

db = DBManager()

users = SafeDict()  # Global storage of users data

last_msg_time = dict()

bot = telebot.TeleBot(TOKEN)

def get_text_from_kb(chat_id, callback):
    '''
    Get text for messages in Inline Keyboards
    '''
    for kb in users.get(chat_id, 'keyboard'):
        for btn in kb:
            if btn['callback_data'] == callback:
                return btn['text']


def send_and_save_msg(chat_id, text, markup):
    '''
    Send message and saves its message_id and markup
    '''
    msg = bot.send_message(chat_id, text, reply_markup=markup)
    users.set(msg.chat.id, 'msg_id', msg.message_id)
    users.set(msg.chat.id, 'keyboard', markup.keyboard)


def delete_msg(chat_id, text=''):
    '''
    Delete the message and send 'text' if it not empty
    '''
    bot.delete_message(chat_id, users.get(chat_id, 'msg_id'))
    if text:
        bot.send_message(chat_id, text)

def send_slowly(chat_id, text, reply_markup=None, parse_mode='Markdown', retry=False):
    t1 = last_msg_time.get(chat_id) or 0.1
    t2 = time.time()
    if t2 - t1 > 0.3:
        bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)
        last_msg_time[chat_id] = time.time()


#  Messages handlers


@bot.message_handler(commands=['start'])
def start_msg(message):
    '''
    Handler for the "/start" command.
    '''
    if not db.today_timetable(message.from_user.id):
        send_slowly(message.chat.id, answ.reg_0, reply_markup=RmKeyboard.markup)
        send_and_save_msg(message.chat.id, answ.reg_1, QualKeyboard.markup)
    else:
        send_slowly(message.chat.id, answ.start, reply_markup=MainKeyboard.markup)


@bot.message_handler(commands=['help'])
def help_msg(message):
    '''
    Handler for the "/help" command.
    '''
    send_slowly(message.chat.id, answ.help_msg, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[0])
@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[1])
def sched_on_day(message):
    '''
    Handler for the command "schedule for today / tomorrow"
    '''
    tommorow = int(message.text == MainKeyboard.btns_text[1])
    msg = answ(message.chat.id).today_msg(tommorow)
    send_slowly(message.chat.id, msg, parse_mode='Markdown')
    db.add_message(message.chat.id, message.text)


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[2])
def sched_on_week(message):
    '''
    Handler for the command "schedule for week"
    '''
    send_slowly(message.chat.id, answ.weekday, reply_markup=WeekKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text in WeekKeyboard.btns_text)
def week_msg(message):
    '''
    Handler for the command "schedule for the day of week"
    '''
    index = WeekKeyboard.btns_text.index(message.text)
    weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    msg = answ(message.chat.id).week_msg(weekdays[index])
    send_slowly(message.chat.id, msg, parse_mode='Markdown', reply_markup=MainKeyboard.markup)
    db.add_message(message.chat.id, message.text)


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[3])
def bells_msg(message):
    '''
    Handler for the command "schedule of bells"
    '''
    send_slowly(message.chat.id, answ.bells, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[4])
def settings_msg(message):
    '''
    Handler for the command "settings"
    '''
    send_slowly(message.chat.id, answ.settings, reply_markup=SettingsKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[0])
def set_sched(message):
    '''
    Handler for the command "settings of timetable"
    '''
    send_slowly(message.chat.id, 'Выберите действие:', reply_markup=SetSchedKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[1])
def feedback_msg(message):
    '''
    Handler for the command "feedback"
    '''
    send_slowly(message.chat.id, answ.feedback, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[2])
def updates_msg(message):
    '''
    Handler for the command "updates"
    '''
    send_slowly(message.chat.id, answ.updates, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[3])
def back_msg(message):
    '''
    Handler for the command "back"
    '''
    send_slowly(message.chat.id, answ.back_button, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SetSchedKeyboard.btns_text[0])
def add_schd(message):
    '''
    Handler for the command "add timetable"
    '''
    send_slowly(message.chat.id, answ.add_select, reply_markup=RmKeyboard.markup)
    send_and_save_msg(message.chat.id, answ.reg_1, QualKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SetSchedKeyboard.btns_text[1])
def del_schd(message):
    '''
    Handler for the command "remove timetable"
    '''
    chat_id = message.chat.id
    send_and_save_msg(message.chat.id, answ.del_select, DeleteSchdKeyboard(chat_id).markup)


@bot.message_handler(func=lambda msg: msg.text == SetSchedKeyboard.btns_text[2])
def change_msg(message):
    '''
    Handler for the command "change timetable"
    '''
    send_slowly(message.chat.id, answ.develop, reply_markup=MainKeyboard.markup)


@bot.message_handler(commands=['sendtoall'])
def send_to_all(message):
    '''
    Handler for the "/sendtoall" command.
    '''
    users = db.get_users_list()
    text = message.text.replace('/sendtoall', '')
    if text and message.chat.id == 161084366:
        for i in users:
            try:
                bot.send_message(i, text, parse_mode='Markdown', reply_markup=MainKeyboard.markup)
                time.sleep(0.05)
            except telebot.apihelper.ApiException:
                continue


@bot.message_handler(func=lambda msg: True)
def error_msg(message):
    '''
    Handler for the unknown commands
    '''
    bot.reply_to(message, answ.error, reply_markup=MainKeyboard.markup)


#  Callbacks handlers


@bot.callback_query_handler(func=lambda call: call.data in ('spo', 'bachelors'))
def set_qual(call):
    '''
    Handler for callback with choice of qualification
    '''
    users.set(call.from_user.id, 'qual', call.data)
    # Send select of course
    if call.data == 'spo':
        markup = CourseKeyboards.spo
    else:
        markup = CourseKeyboards.bach
    msg_text = get_text_from_kb(call.from_user.id, call.data)
    delete_msg(call.from_user.id, msg_text)
    send_and_save_msg(call.from_user.id, answ.reg_2, markup)


@bot.callback_query_handler(func=lambda call: 'del_' in call.data)
def delete_schedule(call):
    '''
    Handler for callback with choice of timetable to be removed
    '''
    msg_text = get_text_from_kb(call.from_user.id, call.data)
    delete_msg(call.from_user.id, msg_text)
    if len(db.today_timetable(call.from_user.id)) == 1:
        msg_text = answ.del_one_error
    else:
        msg_text = answ.del_succses if int(db.rm_timetable(call.data[4:])) else answ.del_wtf
    bot.send_message(call.from_user.id, msg_text, reply_markup=MainKeyboard.markup)


@bot.callback_query_handler(func=lambda call: int(call.data) in range(1, 6))
def set_course(call):
    '''
    Handler for callback with choice of course
    '''
    users.set(call.from_user.id, 'course', call.data)
    # Send select of group
    markups = {
        'spo': {
            '1': SpoGroups.first,
            '2': SpoGroups.second,
            '3': SpoGroups.third,
            '4': SpoGroups.fourth
        },
        'bachelors': {
            '1': BachelorsGroups.first,
            '2': BachelorsGroups.second,
            '3': BachelorsGroups.third,
            '4': BachelorsGroups.fourth,
            '5': BachelorsGroups.fifth
        }
    }
    markup = markups[users.get(call.from_user.id, 'qual')][call.data]
    msg_text = get_text_from_kb(call.from_user.id, call.data)
    delete_msg(call.from_user.id, msg_text)
    send_and_save_msg(call.from_user.id, answ.reg_3, markup)


@bot.callback_query_handler(func=lambda call: int(call.data) in range(11, 53))
def set_group(call):
    '''
    Handler for callback with choice of group
    '''
    users.set(call.from_user.id, 'group', call.data)
    # Write data in database
    data = users.get(call.from_user.id)
    db.add_timetable(call.from_user.id, data['qual'], data['course'], data['group'])
    # End of registration
    msg_text = get_text_from_kb(call.from_user.id, call.data)
    delete_msg(call.from_user.id, msg_text)
    bot.send_message(call.from_user.id, answ.reg_4, reply_markup=MainKeyboard.markup)

app = web.Application()

async def handle(request):
    '''
     Handler for webhooks
    '''
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    return web.Response(status=403)

app.router.add_post('/{token}/', handle)

if __name__ == "__main__":
    bot.remove_webhook()
    if USE_LONG_POLLING:
        bot.polling()
    else:
        bot.set_webhook(url=URL)
        web.run_app(app, port=WH_PORT,)
