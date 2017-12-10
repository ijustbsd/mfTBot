# -*- coding: utf-8 -*-
'''
Bot config file. Before using, remove "sample_" from the file name!
'''

TOKEN = "PASTE YOUR TOKEN HERE"

USE_LONG_POLLING = True  # Change on False for using webhooks

WH_HOST = '<ip/host where the bot is running>'
WH_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WH_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WH_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WH_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

URL = "https://{}:{}/{}/".format(WH_HOST, WH_PORT, TOKEN)
