from datetime import datetime

from libs.db import DBManager

reg_msg_0 = 'Привет! Похоже я не знаю тебя \U0001F614'
reg_msg_1 = 'Выбери квалификацию:'
reg_msg_2 = 'Выбери свой курс:'
reg_msg_3 = 'Теперь выбери группу или направление:'
reg_msg_4 = 'Отлично! На этом всё! Приятного использования \U0001F60A'
start_msg = 'Привет! Я помогу тебе узнать расписание, обращайся \U0001f609'
error_msg = 'К сожалению, я тебя не понимаю \U0001f622'
settings_msg = 'Что нужно сделать?'
back_button_msg = '\U0001F519 В главное меню'
again_msg = 'Заполни данные ещё раз:'
feedback_msg = """
Нужно поменять расписание?
Нашли неприятный баг?
Есть предложения по улучшению работы бота?
Напишите мне в ЛС @ijustbsd !
"""
updates_msg = """
Вы можете следить за новостями и обновлениями бота здесь:
t.me/mathfuck\_news
"""

stats_msg = """
*За сегодня:*
Зарегистрировалось: {}
Сообщений: {}
Пользователей: {}

*За всё время:*
Зарегистрировалось: {}
Сообщений: {}
"""


def get_stats_msg():
    db = DBManager()
    output = []
    query = "SELECT COUNT(*) FROM users WHERE regdate = '{}'".format(
        str(datetime.now().date()))
    output.append(*db.query(query).fetchone())
    query = "SELECT COUNT(*) FROM messages WHERE\
        command LIKE '%Се%' OR\
        command LIKE '%З%' OR\
        command LIKE '%на%' OR\
        command LIKE '%зв%'"
    output.append(*db.query(query).fetchone())
    query = "SELECT chatid FROM messages GROUP BY chatid HAVING COUNT(*) > 0"
    output.append(len(db.query(query).fetchall()))
    query = "SELECT COUNT(*) FROM users"
    output.append(*db.query(query).fetchone())
    query = "SELECT COUNT(*) FROM messages WHERE\
        command LIKE '%Се%' OR\
        command LIKE '%З%' OR\
        command LIKE '%на%' OR\
        command LIKE '%зв%' AND msgdate = '{}'".format(str(datetime.now().date()))
    output.append(*db.query(query).fetchone())
    return stats_msg.format(*output)
