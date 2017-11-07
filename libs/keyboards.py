# -*- coding: utf-8 -*-

from telebot import types

class MainKeyboard:
    btns_text = (
        '\U0001F4D8 Сегодня',
        '\U0001F4D7 Завтра',
        '\U0001F4C5 Расписание на другие дни',
        '\U0001f514 Расписание звонков',
        '\U0001f6e0 Настройки')

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
        '\U0001f4da Настроить расписание',
        '\U0001f4dd Обратная связь',
        '\U0001f300 Обновления',
        '\U0001f519 В главное меню')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for s in btns_text:
        markup.row(s)


class SetSchedKeyboard:
    btns_text = (
        '\u002B Добавить расписание',
        '\u2212 Удалить расписание',
        '\U0001f4b1 Изменить расписание',
        '\U0001f519 В главное меню')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for s in btns_text:
        markup.row(s)


class RmKeyboard:
    markup = types.ReplyKeyboardRemove()
