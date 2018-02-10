# -*- coding: utf-8 -*-
'''
Main file. Run it for bot start working.
'''

import datetime
import logging
import ssl

import telebot
from aiohttp import web

from libs.db import DBManager
from libs.safedict import SafeDict
from libs.keyboards import (
    MainKeyboard, WeekKeyboard, SettingsKeyboard, SetSchedKeyboard, RmKeyboard,
    QualKeyboard, CourseKeyboards, BachelorsGroups, SpoGroups, DeleteSchdKeyboard)
from libs.answers import Answers as answ
from config import TOKEN, USE_LONG_POLLING, URL, WH_SSL_CERT, WH_SSL_PRIV, WH_PORT

logger = telebot.logger
telebot.logger.setLevel(logging.ERROR)

db = DBManager()

users = SafeDict()  # Global storage of users data

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


#  Messages handlers


@bot.message_handler(commands=['start'])
def start_msg(message):
    '''
    Handler for the "/start" command.
    '''
    if not db.today_timetable(message.from_user.id):
        bot.send_message(message.chat.id, answ.reg_0, reply_markup=RmKeyboard.markup)
        send_and_save_msg(message.chat.id, answ.reg_1, QualKeyboard.markup)
    else:
        bot.send_message(message.chat.id, answ.start, reply_markup=MainKeyboard.markup)


@bot.message_handler(commands=['help'])
def help_msg(message):
    '''
    Handler for the "/help" command.
    '''
    bot.send_message(message.chat.id, answ.help_msg, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[0])
@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[1])
def sched_on_day(message):
    '''
    Handler for the command "schedule for today / tomorrow"
    '''
    tommorow = int(message.text == MainKeyboard.btns_text[1])
    msg = answ(message.chat.id).today_msg(tommorow)
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[2])
def sched_on_week(message):
    '''
    Handler for the command "schedule for week"
    '''
    bot.send_message(message.chat.id, answ.weekday, reply_markup=WeekKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text in WeekKeyboard.btns_text)
def week_msg(message):
    '''
    Handler for the command "schedule for the day of week"
    '''
    index = WeekKeyboard.btns_text.index(message.text)
    weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    msg = answ(message.chat.id).week_msg(weekdays[index])
    bot.send_message(message.chat.id, msg, parse_mode='Markdown', reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[3])
def bells_msg(message):
    '''
    Handler for the command "schedule of bells"
    '''
    bot.send_message(message.chat.id, answ.bells, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[4])
def settings_msg(message):
    '''
    Handler for the command "settings"
    '''
    bot.send_message(message.chat.id, answ.settings, reply_markup=SettingsKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[0])
def set_sched(message):
    '''
    Handler for the command "settings of timetable"
    '''
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=SetSchedKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[1])
def feedback_msg(message):
    '''
    Handler for the command "feedback"
    '''
    bot.send_message(message.chat.id, answ.feedback, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[2])
def updates_msg(message):
    '''
    Handler for the command "updates"
    '''
    bot.send_message(message.chat.id, answ.updates, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[3])
def back_msg(message):
    '''
    Handler for the command "back"
    '''
    bot.send_message(message.chat.id, answ.back_button, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SetSchedKeyboard.btns_text[0])
def add_schd(message):
    '''
    Handler for the command "add timetable"
    '''
    bot.send_message(message.chat.id, answ.add_select, reply_markup=RmKeyboard.markup)
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
    bot.send_message(message.chat.id, answ.develop, reply_markup=MainKeyboard.markup)


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

if USE_LONG_POLLING:
    bot.polling()
else:
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

    bot.remove_webhook()

    bot.set_webhook(url=URL, certificate=open(WH_SSL_CERT, 'r'))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WH_SSL_CERT, WH_SSL_PRIV)

    web.run_app(app, port=WH_PORT, ssl_context=context,)
