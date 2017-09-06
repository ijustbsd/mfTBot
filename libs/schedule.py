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


def load_schedule(user_id):
    user = load_user(user_id)
    course = user["course"]
    group = user["group"]
    with open('%s/%s/%s.json' % (str(PATH), course, group)) as json_file:
        schedule = json.load(json_file)
    num_sch = ['\n'.join(i) for i in schedule["numerator"]]
    denom_sch = ['\n'.join(i) for i in schedule["denominator"]]
    return (num_sch, denom_sch)


def today_schedule(user_id, tomorrow=0):
    schedule = load_schedule(user_id)
    today = datetime.date.today() + datetime.timedelta(days=tomorrow)
    weekday = today.weekday()
    is_numerator = today.isocalendar()[1] % 2
    return schedule[int(not is_numerator)][weekday]


def week_schedule(user_id, index):
    schedule = load_schedule(user_id)
    if schedule[0][index] == schedule[1][index]:
        return days_schedule[index] + schedule[0][index]
    else:
        return '%s*Числитель:*\n%s\n\n*Знаменатель:*\n%s' % (
            days_schedule[index],
            schedule[0][index],
            schedule[1][index]
        )
