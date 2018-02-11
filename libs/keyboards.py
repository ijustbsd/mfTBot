# -*- coding: utf-8 -*-
'''
Keyboards and inline keyboards storage.
'''

from telebot import types
from libs.db import DBManager

class MainKeyboard:
    '''
    Main keyboard in bot
    '''
    btns_text = (
        '\U0001F4D8 Сегодня',
        '\U0001F4D7 Завтра',
        '\U0001F4C5 Расписание на другие дни',
        '\U0001f514 Расписание звонков',
        '\U0001f6e0 Настройки')

    markup = types.ReplyKeyboardMarkup()
    markup.row(*btns_text[:2])
    for s in btns_text[2:]:
        markup.row(s)


class WeekKeyboard:
    '''
    Keyboard with days of the week
    '''
    btns_text = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суббота', 'Воскресенье')

    markup = types.ReplyKeyboardMarkup()
    markup.row(*btns_text[:5])
    for s in btns_text[5:]:
        markup.row(s)


class SettingsKeyboard:
    '''
    Keyboard with settings commands
    '''
    btns_text = (
        '\U0001f4da Настроить расписание',
        '\U0001f4dd Обратная связь',
        '\U0001f300 Обновления',
        '\U0001f519 В главное меню')

    markup = types.ReplyKeyboardMarkup()
    for s in btns_text:
        markup.row(s)


class SetSchedKeyboard:
    '''
    Keyboard with settings of schedules
    '''
    btns_text = (
        '\u002B Добавить расписание',
        '\u2212 Удалить расписание',
        '\U0001f4b1 Изменить расписание',
        '\U0001f519 В главное меню')

    markup = types.ReplyKeyboardMarkup()
    for s in btns_text:
        markup.row(s)


class RmKeyboard:
    '''
    Remove keyboard
    '''
    markup = types.ReplyKeyboardRemove()


class QualKeyboard:
    '''
    Inline keyboard for select of qualification
    '''
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(text='СПО', callback_data='spo'),
        types.InlineKeyboardButton(text='Бакалавр', callback_data='bachelors'))


class CourseKeyboards:
    '''
    Inline keyboards for select of course
    '''
    spo = types.InlineKeyboardMarkup()
    spo_btns = []
    for i in range(1, 5):
        spo_btns.append(types.InlineKeyboardButton(text=str(i), callback_data=str(i)))
    spo.row(*spo_btns)

    bach = types.InlineKeyboardMarkup()
    bach_btns = []
    for i in range(1, 6):
        bach_btns.append(types.InlineKeyboardButton(text=str(i), callback_data=str(i)))
    bach.row(*bach_btns)


class BachelorsGroups:
    '''
    Inline keyboards for bachelors
    '''
    first = types.InlineKeyboardMarkup()  # First course
    first.row(
        types.InlineKeyboardButton(text='1.1', callback_data='11'),
        types.InlineKeyboardButton(text='1.2', callback_data='12'))
    first.row(types.InlineKeyboardButton(text='2.1', callback_data='21'))
    first.row(
        types.InlineKeyboardButton(text='3.1', callback_data='31'),
        types.InlineKeyboardButton(text='3.2', callback_data='32'),
        types.InlineKeyboardButton(text='3.3', callback_data='33'))
    first.row(types.InlineKeyboardButton(text='4.1', callback_data='41'))
    first.row(
        types.InlineKeyboardButton(text='5.1', callback_data='51'),
        types.InlineKeyboardButton(text='5.2', callback_data='52'))

    second = types.InlineKeyboardMarkup()  # Second course
    second.row(
        types.InlineKeyboardButton(text='1.1', callback_data='11'),
        types.InlineKeyboardButton(text='1.2', callback_data='12'))
    second.row(types.InlineKeyboardButton(text='2.1', callback_data='21'))
    second.row(
        types.InlineKeyboardButton(text='3.1', callback_data='31'),
        types.InlineKeyboardButton(text='3.2', callback_data='32'),
        types.InlineKeyboardButton(text='3.3', callback_data='33'))
    second.row(
        types.InlineKeyboardButton(text='4.1', callback_data='41'),
        types.InlineKeyboardButton(text='4.2', callback_data='42'))
    second.row(
        types.InlineKeyboardButton(text='5.1', callback_data='51'),
        types.InlineKeyboardButton(text='5.2', callback_data='52'))

    third = types.InlineKeyboardMarkup()  # Third course
    third.row(
        types.InlineKeyboardButton(text='КАТМА', callback_data='11'),
        types.InlineKeyboardButton(text='КУЧП', callback_data='12'))
    third.row(types.InlineKeyboardButton(text='КММ', callback_data='21'))
    third.row(
        types.InlineKeyboardButton(text='КМА ММЭ', callback_data='31'),
        # types.InlineKeyboardButton(text='КМА ММЭ (3.2)', callback_data='32'),
        types.InlineKeyboardButton(text='КФА', callback_data='33'))
    third.row(
        types.InlineKeyboardButton(text='КТФ', callback_data='41'),
        types.InlineKeyboardButton(text='КМА МАиП', callback_data='42'))

    fourth = types.InlineKeyboardMarkup()  # Fourth course
    fourth.row(
        types.InlineKeyboardButton(text='КАТМА', callback_data='11'),
        types.InlineKeyboardButton(text='КУЧП', callback_data='12'))
    fourth.row(types.InlineKeyboardButton(text='КММ', callback_data='21'))
    fourth.row(
        types.InlineKeyboardButton(text='КМА ММЭ', callback_data='31'),
        types.InlineKeyboardButton(text='КМА МАиП', callback_data='42'),
        types.InlineKeyboardButton(text='КФА', callback_data='33'))
    fourth.row(types.InlineKeyboardButton(text='КТФ', callback_data='41'))

    fifth = types.InlineKeyboardMarkup()  # Fifth course
    fifth.row(
        types.InlineKeyboardButton(text='КММ', callback_data='21'))
        # types.InlineKeyboardButton(text='КТФ', callback_data='41'),
        # types.InlineKeyboardButton(text='КМА МАиП', callback_data='42'))


class SpoGroups:
    '''
    Inline keyboards for SPO
    '''
    first = types.InlineKeyboardMarkup()  # First course
    first.row(
        types.InlineKeyboardButton(text='ПКС-1', callback_data='11'),
        types.InlineKeyboardButton(text='ПКС-2', callback_data='12'))
    first.row(types.InlineKeyboardButton(text='ЭБУ', callback_data='21'))

    second = types.InlineKeyboardMarkup()  # Second course
    second.row(types.InlineKeyboardButton(text='ПКС', callback_data='11'))
    second.row(
        types.InlineKeyboardButton(text='ЭБУ-1', callback_data='21'),
        types.InlineKeyboardButton(text='ЭБУ-2', callback_data='22'))

    third = types.InlineKeyboardMarkup()  # Third course
    third.row(types.InlineKeyboardButton(text='ПКС', callback_data='11'))
    third.row(types.InlineKeyboardButton(text='ЭБУ', callback_data='21'))

    fourth = types.InlineKeyboardMarkup()  # Fourth course
    fourth.row(types.InlineKeyboardButton(text='ПКС', callback_data='11'))


class DeleteSchdKeyboard:
    '''
    Inline keyboards for SPO
    '''
    def __init__(self, chat_id):
        db = DBManager()
        ttable = db.today_timetable(chat_id)
        self.markup = types.InlineKeyboardMarkup()
        for tt in ttable:
            text = tt['text']
            callback = 'del_{}'.format(tt['_id'])
            self.markup.row(
                types.InlineKeyboardButton(
                    text='{}, {} курс, группа {}'.format(*text), callback_data=callback))
