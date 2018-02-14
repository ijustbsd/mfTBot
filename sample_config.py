# -*- coding: utf-8 -*-
'''
Bot config file. Before using, remove "sample_" from the file name!
'''

TOKEN = "PASTE YOUR TOKEN HERE"

USE_LONG_POLLING = True  # Change on False for using webhooks

WH_HOST = '<ip/host where the bot is running>'
WH_PORT = 8443

URL = "https://{}/{}/".format(WH_HOST, TOKEN)

DB_USER = 'username'
DB_PWD = 'password'
DB_NAME = 'vsumfbot'
