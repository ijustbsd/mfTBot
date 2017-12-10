# -*- coding: utf-8 -*-
'''
Working with database.
'''

import datetime

import pymongo
from bson.objectid import ObjectId

class DBManager():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient()
        except pymongo.errors.ConnectionFailure as e:
            print(e)
        self.db = self.client.mfbot_db
        #  Collections
        self.g_ttables = self.db.general_timetables
        self.u_ttables = self.db.users_timetables
        self.users = self.db.users
        self.messages = self.db.messages


    def load_user(self, chatid: int):
        return self.users.find_one({"chatid": chatid})


    def update_user(self, data):
        return self.users.update_one({'chatid': data['chatid']}, {'$set': data}, upsert=True)


    def add_message(self, chatid: int, text):
        msg = {
            'from': chatid,
            'text': text,
            'date': str(datetime.datetime.utcnow())
        }
        return self.messages.insert_one(msg)


    def add_timetable(self, chatid: int, qual, course, group):
        tt = {'chatid': chatid, 'qualification': qual, 'course': course, 'group': group}
        if self.u_ttables.find_one(tt):
            return
        ttable = self.g_ttables.find_one({'qualification': qual, 'course': course, 'group': group})
        ttable.pop('_id', None)
        doc = {'chatid': chatid}
        doc.update(ttable)
        return self.u_ttables.insert_one(doc).inserted_id


    def rm_timetable(self, _id):
        return self.u_ttables.delete_one({'_id': ObjectId(_id)}).deleted_count


    def today_timetable(self, chatid, tomorrow=0):
        today = datetime.date.today() + datetime.timedelta(days=tomorrow)
        weekday = today.weekday()
        is_numerator = today.isocalendar()[1] % 2
        result = ()
        for tt in self.u_ttables.find({'chatid': chatid}):
            result += ({
                '_id': tt['_id'],
                'text': (tt['qualification_title'], tt['course'], tt['group_title']),
                'data': tt['data']['numerator' if is_numerator else 'denominator'][weekday]
            },)
        # Result format
        # result = ({
        #     'data': [['1', 'title', 'hall', 'teacher'], ['2', '', '', '']],
        #     'text': ('qualification', 'course', 'group')
        # },)
        return result


    def week_timetable(self, chatid, index):
        days = ('понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу', 'воскресенье')
        result = (days[index],)
        for tt in self.u_ttables.find({'chatid': chatid}):
            if tt['data']['numerator'][index] == tt['data']['denominator'][index]:
                result += ({
                    'text': (tt['qualification_title'], tt['course'], tt['group_title']),
                    'data': (tt['data']['numerator'][index],)
                },)
            else:
                result += ({
                    'text': (tt['qualification_title'], tt['course'], tt['group_title']),
                    'data': (tt['data']['numerator'][index], tt['data']['denominator'][index])
                },)
        # Result format
        # result = ('понедельник', {
        #     'data': ([['1', 'title', 'hall', 'teacher'], ['2', '', '', '']],),
        #     'text': ('qualification', 'course', 'group')
        # })
        return result
