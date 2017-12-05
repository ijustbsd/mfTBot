'''
Bot's answers
'''

from libs.db import DBManager

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
    help_msg = (
        '*Справка:*\n'
        '*1.* Чтобы узнать расписание, используйте кнопки ниже.\n\n'
        '*2.* Чтобы изменить расписание нажмите:\n'
        'Настройки → Настроить расписание → Изменить расписание')

    def __init__(self, chatid):
        self.chatid = chatid
        self.db = DBManager()

    def _formatter(self, lessons):
        result = ''
        for l in lessons:
            result += '{num}. {title} {hall}\n'.format(
                num=l[0],
                title=l[1] or '-',
                hall='\[Ауд. ' + l[2] + ']' if l[2] else ''
            )
            if result == '. - \n':
                result = 'Выходной :)'
        return result

    def today_msg(self, tomorrow=0):
        ttable = self.db.today_timetable(self.chatid, tomorrow)
        result = '*Расписание на {}:*\n'.format('завтра' if tomorrow else 'сегодня')
        group_title = '*({}, {} курс, группа {})*\n' if len(ttable) != 1 else ''
        for tt in ttable:
            result += group_title.format(*tt['text']) + self._formatter(tt['data']) + '\n'
        return result

    def week_msg(self, index):
        ttable = self.db.week_timetable(self.chatid, index)
        result = '*Расписание на ' + ttable[0] + ':*\n'
        group_title = '\n*({}, {} курс, группа {})*\n' if len(ttable) != 1 else ''
        for tt in ttable[1:]:
            if len(tt['data']) == 1:
                result += group_title.format(*tt['text']) + self._formatter(tt['data'][0]) + '\n'
            else:
                result += group_title.format(*tt['text']) +\
                '*Числитель:*\n' + self._formatter(tt['data'][0]) +\
                '*Знаменатель:*\n' + self._formatter(tt['data'][1])
        return result
