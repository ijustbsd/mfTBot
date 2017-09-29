import sqlite3
from config import PATH

users = """
CREATE TABLE IF NOT EXISTS 'users' (
'chatid' INTEGER NOT NULL,
'firstname' TEXT,
'lastname' TEXT,
'username' TEXT,
'regdate' TEXT
)
"""

messages = """
CREATE TABLE IF NOT EXISTS 'messages' (
'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
'chatid' INTEGER NOT NULL,
'command' TEXT NOT NULL,
'msgdate' TEXT NOT NULL,
'msgtime' TEXT NOT NULL
)
"""

schedules = """
CREATE TABLE IF NOT EXISTS 'schedules' (
'chatid' INTEGER NOT NULL,
'faculty' TEXT NOT NULL,
'qual' TEXT NOT NULL,
'course' TEXT NOT NULL,
'groupa' TEXT NOT NULL
)
"""

tables = (users, messages, schedules)


class DBManager():
    def __init__(self):
        try:
            self.connect = sqlite3.connect(PATH + '/data/db.sqlite3')
        except sqlite3.Error as e:
            print(e)
        self.cursor = self.connect.cursor()
        for t in tables:
            self.cursor.execute(t)

    def query(self, arg):
        self.cursor.execute(arg)
        self.connect.commit()
        return self.cursor

    def __del__(self):
        self.connect.close()
