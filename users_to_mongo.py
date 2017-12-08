'''
Temporary bullshit :D
'''
import sqlite3
from libs.db import DBManager

db = DBManager()

connect = sqlite3.connect('data/db.sqlite3')
cursor = connect.cursor()
query = cursor.execute('SELECT * FROM users')
for row in query:
    print(row)
    userdata = {
        'chatid': row[0],
        'firstname': row[1],
        'lastname': row[2],
        'username': row[3],
        'regdate': row[4]
    }
    db.update_user(userdata)
connect.commit()
