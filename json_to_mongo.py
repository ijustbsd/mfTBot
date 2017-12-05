"""
Temporary bullshit :D
"""
import os
import json
from pathlib import Path

import pymongo

class JSONTest():
    def __init__(self):
        self.path = str(Path(__file__).parents[0]) + '/data/timetables/'

        self.files = []
        for path, _dirs, files in os.walk(self.path):
            for name in files:
                self.files.append(os.path.join(path, name))

        self.client = pymongo.MongoClient()
        self.db = self.client.mfbot_db
        self.g_ttables = self.db.general_timetables

        self.complete = True
        for f in self.files:
            self.write_to_db(f)

    def get_string(self, data):
        res = ()
        for i in data:
            num = i.split('.')[0]
            try:
                aud = i.split('[')[1][5:-1]
                title = i.split('[')[0][3:-2]
            except Exception:
                aud = ''
                title = i.split('[')[0][3:]
            prepod = ''
            if title == '-':
                title = ''

            if i == "Выходной :)":
                num = ''
                title = ''
                aud = ''
                prepod = ''

            res += ((num, title, aud, prepod),)
        print(res)
        return res


    def write_to_db(self, path):
        data = path.split('/')[3:]
        qual = data[0]
        course = data[1]
        group = data[2][:-5]

        qual_title = {
            'bach': 'Бакалавр',
            'spo': 'СПО'
        }

        bach_dir = {
            "11": "КАТМА",
            "12": "КУЧП",
            "21": "КММ",
            "31": "КМА ММЭ (3.1)",
            "32": "КМА ММЭ (3.2)",
            "33": "КФА",
            "41": "КТФ",
            "42": "КМА МАиП"
        }
        spo_dir = {
            "11": "ПКС-1",
            "12": "ПКС-2",
            "21": "ЭБУ-1",
            "22": "ЭБУ-2"
        }
        quals = {"spo": spo_dir, "bach": bach_dir}

        if qual == 'spo':
            g_title = quals[qual][group]
        else:
            if int(course) > 2:
                g_title = quals[qual][group]
            else:
                g_title = '.'.join(group)

        data = {
            'numerator': (),
            'denominator': ()
        }

        with open(path) as file:
            js = json.load(file)
            for i in js['numerator']:
                data['numerator'] += (self.get_string(i),)
            for i in js['denominator']:
                data['denominator'] += (self.get_string(i),)

        test_db = {
            'faculty': 'math',
            'faculty_title': 'Математический',
            'qualification': qual,
            'qualification_title': qual_title[qual],
            'course': course,
            'group': group,
            'group_title': g_title,
            'data': data
            }

        print(path)
        self.g_ttables.insert_one(test_db)


if __name__ == "__main__":
    if JSONTest().complete:
        print('JSON loaded successfully!')
