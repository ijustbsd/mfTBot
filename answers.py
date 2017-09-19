from libs.stats import load_stats
reg_msg_0 = 'Привет! Похоже я не знаю тебя \U0001F614'
reg_msg_1 = 'Выбери свой курс:'
reg_msg_2 = 'Теперь выбери группу или направление:'
reg_msg_3 = 'Отлично! На этом всё! Приятного использования \U0001F60A'
start_msg = 'Привет! Я помогу тебе узнать расписание, обращайся \U0001f609'
error_msg = 'К сожалению, я тебя не понимаю \U0001f622'
settings_msg = 'Что нужно сделать?'
back_button_msg = '\U0001F519 Назад'
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
*Статистика:*
*За сегодня:*
Пользователей: %d
Сообщений: %d

*За всё время:*
Пользователей: %d
Сообщений: %d

*Запросы:*
"""


def get_stats_msg():
    stats = load_stats()
    out = stats_msg % (
        stats["today_stats"]["users"], stats["today_stats"]["messages"],
        stats["all_stats"]["users"], stats["all_stats"]["messages"]
    )
    for t in stats["requests"].items():
        reqs = "%s: %d\n" % (t)
        out += reqs
    return out
