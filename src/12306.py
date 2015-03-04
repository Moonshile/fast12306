#coding=utf-8

import requests
import json
import sys
import logging

import config

from core import settings, Query, Captcha, Token, User

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

c = Captcha(session, settings.CAPTCHA_FILE)
c.get(settings.URLS['login_captcha'])
code = raw_input()
print c.check(settings.URLS['check_captcha'], code)

t = Token(session, settings.URL_BASE)
key = t.retrieve_key(settings.URLS['login_token'])
value = t.retrieve_value(key)
print key, value

u = User(session, config.USERNAME, config.PASSWORD, settings.LOGIN_NS, settings.USER_NS)
print u.login(settings.URLS['login'], code, key, value)
print u.passengers(settings.URLS['passengers'])

if ferr:
    # tear down
    ferr.close()
