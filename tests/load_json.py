# -*- coding: utf-8 -*-
'''
Testing loading JSON files in data/timetables/
'''

import os
import json
from pathlib import Path

class JSONTest():
    def __init__(self):
        self.path = str(Path(__file__).parents[1]) + '/data/timetables/'

        self.files = []
        for path, _dirs, files in os.walk(self.path):
            for name in files:
                self.files.append(os.path.join(path, name))

        self.complete = True
        for f in self.files:
            self.test(f)


    def test(self, path):
        try:
            with open(path) as file:
                json.load(file)
        except ValueError as e:
            print('JSON error:')
            print(e)
            print('In file %s:' % (path))
            self.complete = False


if __name__ == "__main__":
    if JSONTest().complete:
        print('JSON loaded successfully!')
