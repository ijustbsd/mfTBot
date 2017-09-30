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
    cols = ('firstname', 'lastname', 'username')
    vals = (chatid, firstname, lastname, username, date)
    query = "INSERT OR IGNORE INTO users VALUES ({}, '{}', '{}', '{}', '{}')"
    db.query(query.format(*vals))
    query = "UPDATE users SET {}='{}', {}='{}', {}='{}' WHERE chatid = {}"
    db.query(query.format(
        cols[0], vals[1],
        cols[1], vals[2],
        cols[2], vals[3], chatid))
