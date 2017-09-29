from datetime import datetime

from libs.db import DBManager


def new_msg(chatid, cmd):
    date = str(datetime.now().date())
    time = str(datetime.now().time())
    db = DBManager()
    cols = ('chatid, command, msgdate, msgtime')
    vals = (chatid, cmd, date, time[:-7])
    query = "INSERT INTO messages ({}) VALUES ({},'{}','{}','{}')".format(
        cols, *vals)
    db.query(query)


def new_user(chatid, firstname, lastname, username):
    date = str(datetime.now().date())
    db = DBManager()
    cols = ('chatid, firstname, lastname, username, regdate')
    vals = (chatid, firstname, lastname, username, date)
    query = "INSERT INTO users ({}) VALUES ({},'{}','{}','{}', '{}')".format(
        cols, *vals)
    db.query(query)
