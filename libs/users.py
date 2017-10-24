from libs.db import DBManager


def add_schedule(user_id, qual, course, group):
    scheds = load_user(user_id)
    if len(scheds) > 4:
        return  # TODO: Output
    for s in scheds:
        if s == (qual, course, group):
            return  # TODO: Output
    db = DBManager()
    cols = ('chatid, faculty, qual, course, groupa')
    vals = (user_id, 'math', qual, course, group)
    query = "INSERT INTO schedules ({}) VALUES ({},'{}','{}',{},{})".format(
        cols, *vals)
    db.query(query)


def del_schedule(user_id, num):
    scheds = load_user(user_id)
    if len(scheds) == 1:
        return 'Нельзя удалить единственное расписание!'
    db = DBManager()
    query = "DELETE FROM schedules WHERE chatid = {} AND qual = '{}' AND course = '{}' AND groupa = '{}'".format(
        user_id, *scheds[int(num)])
    db.query(query)
    return 'Расписание успешно удалено!'


def load_user(user_id):
    user_id = int(user_id)
    result = []
    db = DBManager()
    query = "SELECT qual, course, groupa FROM schedules WHERE chatid = {}".format(user_id)
    for row in db.query(query):
        result.append(row)
    return tuple(result)
