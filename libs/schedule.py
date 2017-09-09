import datetime
import json
from pathlib import Path

from libs.users import load_user

PATH = str(Path(__file__).parents[1]) + '/data/timetables'

days_schedule = (
    '*Расписание на понедельник:*\n',
    '*Расписание на вторник:*\n',
    '*Расписание на среду:*\n',
    '*Расписание на четверг:*\n',
    '*Расписание на пятницу:*\n',
    '*Расписание на субботу:*\n',
    '*Расписание на воскресенье:*\n'
)

bells_schedule = """
*Расписание звонков:*
1. 8:00 - 9:35
2. 9:45 - 11:20
3. 11:30 - 13:05
4. 13:25 - 15:00
5. 15:10 - 16:45
6. 16:55 - 18:30
7. 18:40 - 20:00
8. 20:10 - 21:30
"""


def gr_to_dir(group):
    directions = {
        "11": "КАТМА",
        "12": "КУЧП",
        "21": "КММ",
        "31": "КМА ММЭ (3.1)",
        "32": "КМА ММЭ (3.2)",
        "33": "КФА",
        "41": "КТФ",
        "42": "КМА МАиП"
    }
    return directions[group]


def load_schedule(user_id):
    user = load_user(user_id)
    schedules = []
    for u in user:
        course = u["course"]
        group = u["group"]
        with open('%s/%s/%s.json' % (PATH, course, group)) as json_file:
            schedule = json.load(json_file)
        num_sch = ['\n'.join(i) for i in schedule["numerator"]]
        denom_sch = ['\n'.join(i) for i in schedule["denominator"]]
        schedules.append((num_sch, denom_sch))
    return schedules


def today_schedule(user_id, tomorrow=0):
    schedules = load_schedule(user_id)
    today = datetime.date.today() + datetime.timedelta(days=tomorrow)
    weekday = today.weekday()
    is_numerator = today.isocalendar()[1] % 2
    out_schedule = []
    for x in schedules:
        out_schedule.append(x[int(not is_numerator)][weekday])
    return out_schedule


def week_schedule(user_id, index):
    schedules = load_schedule(user_id)
    out_schedule = []
    for x in schedules:
        if x[0][index] == x[1][index]:
            out_schedule.append(x[0][index])
        else:
            out_schedule.append(
                '*Числитель:*\n%s\n*Знаменатель:*\n%s' % (
                    x[0][index],
                    x[1][index]
                )
            )
    return out_schedule


def schedule_title(user_id):
    user = load_user(user_id)
    titles = []
    for x in user:
        group = '.'.join(x["group"])
        title = 'Курс %s, группа %s' % (x["course"], group)
        if int(x["course"]) > 2:
            group = gr_to_dir(x["group"])
            title = 'Курс %s, %s' % (x["course"], group)
        titles.append(title)
    return titles
