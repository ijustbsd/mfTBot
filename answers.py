"""
Bot's answers
"""

from libs.schedule import (
    today_schedule, week_schedule, schedule_title, days_schedule)

class Answers():
    reg_0 = 'Привет! Похоже я не знаю тебя \U0001F614'
    reg_1 = 'Выбери квалификацию:'
    reg_2 = 'Выбери свой курс:'
    reg_3 = 'Теперь выбери группу или направление:'
    reg_4 = 'Отлично! На этом всё! Приятного использования \U0001F60A'
    reg_error = 'Что-то прошло не так :( Пройдите регистрацию ещё раз!'
    start = 'Привет! Я помогу тебе узнать расписание, обращайся \U0001f609'
    error = 'К сожалению, я тебя не понимаю \U0001f622'
    settings = 'Что нужно сделать?'
    back_button = '\U0001F519 В главное меню'
    again = 'Заполни данные ещё раз:'
    weekday = 'Выберите день недели:'
    feedback = (
        'Нужно поменять расписание?\n'
        'Нашли неприятный баг?\n'
        'Есть предложения по улучшению работы бота?\n'
        'Напишите мне в ЛС @ijustbsd !')
    updates = (
        'Вы можете следить за новостями и обновлениями бота здесь:\n'
        't.me/mfbot_news')
    bells = (
        '*Расписание звонков:*\n'
        '1. 8:00 - 9:35\n'
        '2. 9:45 - 11:20\n'
        '3. 11:30 - 13:05\n'
        '4. 13:25 - 15:00\n'
        '5. 15:10 - 16:45\n'
        '6. 16:55 - 18:30\n'
        '7. 18:40 - 20:00\n'
        '8. 20:10 - 21:30\n')
    add_select = 'Какое расписание нужно добавить?'
    del_select = 'Какое расписание нужно убрать?'
    develop = 'Функция в разработке \U0001F527'

    def __init__(self, chatid):
        self.chatid = chatid

    def today_msg(self, tomorrow=0):
        schedule = today_schedule(self.chatid, tomorrow)
        titles = schedule_title(self.chatid)
        text = 'завтра' if tomorrow else 'сегодня'
        if len(schedule) == 1:
            return ('*Расписание на %s:*\n%s' % (text, schedule[0]), )
        else:
            result = ()
            for s, t in zip(schedule, titles):
                result += ('*Расписание на %s:\n(%s)*\n%s' % (text, t, s), )
        return result

    def week_msg(self, index):
        titles = schedule_title(self.chatid)
        result = days_schedule[index] + '\n'
        for s, t in zip(week_schedule(self.chatid, index), titles):
            result += '*%s*\n%s\n\n' % (t, s)
        return result
