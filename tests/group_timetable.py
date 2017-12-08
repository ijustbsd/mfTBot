# -*- coding: utf-8 -*-
"""
Print all timetables in the group
"""

import pymongo

class GroupTTableTest():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient()
        except pymongo.errors.ConnectionFailure as e:
            print(e)
        self.db = self.client.mfbot_db
        self.g_ttables = self.db.general_timetables


    def _formatter(self, lessons):
        day = ''
        for l in lessons:
            day += '{num}. {title} {hall}\n'.format(
                num=l[0],
                title=l[1] or '-',
                hall='[Ауд. ' + l[2] + ']' if l[2] else ''
            )
        if day == '. - \n':
            day = 'Выходной :)\n'
        return day


    def group_choice(self):
        ttable = self.g_ttables.find().sort([
            ('qualification', pymongo.ASCENDING),
            ('course', pymongo.ASCENDING),
            ('group', pymongo.ASCENDING)])
        index = 0
        ids = ()
        for tt in ttable:
            print('{}. {qualification_title}, {course} курс, группа {group}'.format(
                str(index), **tt))
            ids += (tt['_id'],)
            index += 1
        index = input('Выбери нужную группу: ')
        self.print_timetable(ids[int(index)])


    def print_timetable(self, _id):
        data = self.g_ttables.find_one({'_id': _id})
        print('>>> {qualification_title}, {course} курс, группа {group}'.format(**data))
        data = data['data']
        days = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')
        for i in range(0, 7):
            print('\n[:: ' + days[i] + ' ::]\n')
            if data['numerator'][i] == data['denominator'][i]:
                print(self._formatter(data['numerator'][i]))
            else:
                print(self._formatter(data['numerator'][i]))
                print(self._formatter(data['denominator'][i]))


if __name__ == "__main__":
    GroupTTableTest().group_choice()
