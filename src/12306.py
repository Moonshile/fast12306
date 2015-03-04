#coding=utf-8

import requests
import json
import sys
import logging

import config

from core import settings, Query, Captcha, Token

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d|%(levelname)s|%(message)s',
    datefmt='%Y-%m-%d %X',
    filename=settings.LOGGING_FILE,
)

ferr = None
if settings.DEBUG:
    # redirect stderr to settings.ERR_LOG_FILE
    ferr = open(settings.ERR_LOG_FILE, 'w')
    sys.stderr = ferr

session = requests.Session()
session.timeout = settings.TIMEOUT
session.verify = settings.VERIFY

t = Token(session, 'https://kyfw.12306.cn/')
key = t.retrieve_key('https://kyfw.12306.cn/otn/login/init')
value = t.retrieve_value(key)
print key, value

if ferr:
    # tear down
    ferr.close()
