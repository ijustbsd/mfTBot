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
        self.db = self.client.vsumfbot
        #  Collections
        self.g_ttables = self.db.general_timetables
        self.u_ttables = self.db.users_timetables
        self.messages = self.db.messages


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
        weekday = today.strftime("%A").lower()
        is_numerator = today.isocalendar()[1] % 2
        result = ()
        for tt in self.u_ttables.find({'chatid': chatid}):
            result += ({
                '_id': tt['_id'],
                'text': (tt['qualification_title'], tt['course'], tt['group_title']),
                'data': tt['data'][weekday]['numerator' if is_numerator else 'denominator']
            },)
        # Result format
        # result = ({
        #     'data': [['1', 'title', 'hall', 'teacher'], ['2', '', '', '']],
        #     'text': ('qualification', 'course', 'group')
        # },)
        return result


    def week_timetable(self, chatid, index):
        en_to_ru = {
            'monday': 'понедельник',
            'tuesday': 'вторник',
            'wednesday': 'среду',
            'thursday': 'четверг',
            'friday': 'пятницу',
            'saturday': 'субботу',
            'sunday': 'воскресенье'
        }
        result = (en_to_ru[index],)
        for tt in self.u_ttables.find({'chatid': chatid}):
            if tt['data'][index]['numerator'] == tt['data'][index]['denominator']:
                result += ({
                    'text': (tt['qualification_title'], tt['course'], tt['group_title']),
                    'data': (tt['data'][index]['numerator'],)
                },)
            else:
                result += ({
                    'text': (tt['qualification_title'], tt['course'], tt['group_title']),
                    'data': (tt['data'][index]['numerator'], tt['data'][index]['denominator'])
                },)
        # Result format
        # result = ('понедельник', {
        #     'data': ([['1', 'title', 'hall', 'teacher'], ['2', '', '', '']],),
        #     'text': ('qualification', 'course', 'group')
        # })
        return result

    def get_users_list(self):
        result = set()
        for i in self.u_ttables.find():
            result.update([i['chatid'],])
        return result
