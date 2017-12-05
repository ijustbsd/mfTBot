# -*- coding: utf-8 -*-

import logging
import telebot

from libs.db import DBManager
from libs.safedict import SafeDict
from libs.keyboards import (
    MainKeyboard, WeekKeyboard, SettingsKeyboard, SetSchedKeyboard, RmKeyboard,
    QualKeyboard, CourseKeyboards, BachelorsGroups, SpoGroups, DeleteSchdKeyboard)
from libs.answers import Answers as answ
from config import TOKEN

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


''' Messages handlers '''


@bot.message_handler(commands=['start'])
def start_msg(message):
    if not db.load_user(message.from_user.id):
        bot.send_message(message.chat.id, answ.reg_0, reply_markup=RmKeyboard.markup)
        user = message.from_user
        userdata = {
            'chatid': user.id,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'username': user.username
        }
        db.update_user(userdata)
        send_and_save_msg(message.chat.id, answ.reg_1, QualKeyboard.markup)
    else:
        bot.send_message(message.chat.id, answ.start, reply_markup=MainKeyboard.markup)


@bot.message_handler(commands=['help'])
def help_msg(message):
    bot.send_message(message.chat.id, answ.help_msg, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[0])
@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[1])
def sched_on_day(message):
    tommorow = int(message.text == MainKeyboard.btns_text[1])
    msg = answ(message.chat.id).today_msg(tommorow)
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[2])
def sched_on_week(message):
    bot.send_message(message.chat.id, answ.weekday, reply_markup=WeekKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text in WeekKeyboard.btns_text)
def week_msg(message):
    index = WeekKeyboard.btns_text.index(message.text)
    msg = answ(message.chat.id).week_msg(index)
    bot.send_message(message.chat.id, msg, parse_mode='Markdown', reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[3])
def bells_msg(message):
    bot.send_message(message.chat.id, answ.bells, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[4])
def settings_msg(message):
    bot.send_message(message.chat.id, answ.settings, reply_markup=SettingsKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[0])
def set_sched(message):
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=SetSchedKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[1])
def feedback_msg(message):
    bot.send_message(message.chat.id, answ.feedback, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[2])
def updates_msg(message):
    bot.send_message(message.chat.id, answ.updates, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SettingsKeyboard.btns_text[3])
def back_msg(message):
    bot.send_message(message.chat.id, answ.back_button, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SetSchedKeyboard.btns_text[0])
def add_schd(message):
    bot.send_message(message.chat.id, answ.add_select, reply_markup=RmKeyboard.markup)
    send_and_save_msg(message.chat.id, answ.reg_1, QualKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == SetSchedKeyboard.btns_text[1])
def del_schd(message):
    chat_id = message.chat.id
    send_and_save_msg(message.chat.id, answ.del_select, DeleteSchdKeyboard(chat_id).markup)


@bot.message_handler(func=lambda msg: msg.text == SetSchedKeyboard.btns_text[2])
def change_msg(message):
    bot.send_message(message.chat.id, answ.develop, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: True)
def error_msg(message):
    bot.reply_to(message, answ.error, reply_markup=MainKeyboard.markup)


''' Callbacks handlers '''


@bot.callback_query_handler(func=lambda call: call.data in ('spo', 'bach'))
def set_qual(call):
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
    msg_text = get_text_from_kb(call.from_user.id, call.data)
    delete_msg(call.from_user.id, msg_text)
    if len(db.today_timetable(call.from_user.id)) == 1:
        msg_text = answ.del_one_error
    else:
        msg_text = answ.del_succses if int(db.rm_timetable(call.data[4:])) else answ.del_wtf
    bot.send_message(call.from_user.id, msg_text, reply_markup=MainKeyboard.markup)


@bot.callback_query_handler(func=lambda call: int(call.data) in range(1, 6))
def set_course(call):
    users.set(call.from_user.id, 'course', call.data)
    # Send select of group
    markups = {
        'spo': {
            '1': SpoGroups.first,
            '2': SpoGroups.second,
            '3': SpoGroups.third,
            '4': SpoGroups.fourth
        },
        'bach': {
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
    users.set(call.from_user.id, 'group', call.data)
    # Write data in database
    data = users.get(call.from_user.id)
    db.add_timetable(call.from_user.id, data['qual'], data['course'], data['group'])
    # End of registration
    msg_text = get_text_from_kb(call.from_user.id, call.data)
    delete_msg(call.from_user.id, msg_text)
    bot.send_message(call.from_user.id, answ.reg_4, reply_markup=MainKeyboard.markup)


bot.polling()
