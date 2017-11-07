# -*- coding: utf-8 -*-

from telebot import types

class MainKeyboard:
    btns_text = (
        '\uD83D\uDCD8 Сегодня',
        '\uD83D\uDCD7 Завтра',
        '\uD83D\uDCC5 Расписание на другие дни',
        '\uD83D\uDD14 Расписание звонков',
        '\uD83D\uDEE0 Настройки')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(*btns_text[:2])
    for s in btns_text[2:]:
        markup.row(s)


class WeekKeyboard:
    btns_text = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суббота', 'Воскресенье')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(*btns_text[:5])
    for s in btns_text[5:]:
        markup.row(s)


class SettingsKeyboard:
    btns_text = (
        '\uD83D\uDCDA Настроить расписание',
        '\uD83D\uDCDD Обратная связь',
        '\uD83C\uDF00 Обновления',
        '\uD83D\uDD19 В главное меню')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for s in btns_text:
        markup.row(s)


class SetSchedKeyboard:
    btns_text = (
        '\u002B Добавить расписание',
        '\u2212 Удалить расписание',
        '\uD83D\uDCB1 Изменить расписание',
        '\uD83D\uDD19 В главное меню')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for s in btns_text:
        markup.row(s)


class RmKeyboard:
    markup = types.ReplyKeyboardRemove()
