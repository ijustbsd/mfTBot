# -*- coding: utf-8 -*-
'''
Storage, with synchronizing to database.
'''

import pymongo

from config import DB_USER, DB_PWD, DB_NAME

class SafeDict:
    '''
    Safe dictionary for saving users data
    '''
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(
                username=DB_USER,
                password=DB_PWD,
                authSource=DB_NAME)
        except pymongo.errors.ConnectionFailure as e:
            print(e)
        self.db = self.client.vsumfbot
        self.dict = self.db.safe_dict


    def set(self, chatid, key, value):
        '''
        Set value in the dictionary
        '''
        return self.dict.update_one({'chatid': chatid}, {'$set': {key: value}}, upsert=True)


    def get(self, chatid, key=None):
        '''
        Get value from the dictionary
        '''
        result = self.dict.find_one({'chatid': chatid})
        result.pop('_id', None)
        return result.get(key, result)
