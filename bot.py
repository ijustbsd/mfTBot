# -*- coding: utf-8 -*-

import logging
import telebot

from libs.users import load_user
from libs.keyboards import (
    MainKeyboard, WeekKeyboard, SettingsKeyboard, SetSchedKeyboard, RmKeyboard)
from answers import Answers as answ
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console

@bot.message_handler(commands=['start'])
def start_msg(message):
    if not load_user(message.from_user.id):
        bot.send_message(message.chat.id, answ.reg_0, reply_markup=RmKeyboard.markup)
        # registration()
    else:
        bot.send_message(message.chat.id, answ.start, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[0])
@bot.message_handler(func=lambda msg: msg.text == MainKeyboard.btns_text[1])
def sched_on_day(message):
    tommorow = int(message.text == MainKeyboard.btns_text[1])
    schedules = answ(message.chat.id).today_msg(tommorow)
    for sched in schedules:
        bot.send_message(message.chat.id, sched, parse_mode='Markdown')


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
    # self.registration(chatid)


@bot.message_handler(func=lambda msg: msg.text == SetSchedKeyboard.btns_text[1])
def del_schd(message):
    bot.send_message(message.chat.id, answ.del_select, reply_markup=RmKeyboard.markup)
    # rm msg


@bot.message_handler(func=lambda msg: msg.text == SetSchedKeyboard.btns_text[2])
def change_msg(message):
    bot.send_message(message.chat.id, answ.develop, reply_markup=MainKeyboard.markup)


@bot.message_handler(func=lambda msg: True)
def error_msg(message):
    bot.reply_to(message, answ.error, reply_markup=MainKeyboard.markup)

bot.polling()
