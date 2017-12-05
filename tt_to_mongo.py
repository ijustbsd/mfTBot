'''
Temporary bullshit :D
'''
import sqlite3
from libs.db import DBManager

db = DBManager()

connect = sqlite3.connect('data/db.sqlite3')
cursor = connect.cursor()
query = cursor.execute('SELECT * from schedules')
for row in query:
    print(row)
    db.add_timetable(int(row[0]), row[2], row[3], row[4])
connect.commit()
