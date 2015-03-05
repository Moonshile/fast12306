#coding=utf-8

import requests
import json
import sys
import logging
import time

import config

from core import settings, StationName, Query, Captcha, Token, User, Order

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

# preparation

session = requests.Session()
session.timeout = settings.TIMEOUT
session.verify = settings.VERIFY
session.get(settings.URLS['entry'])
print session.cookies

c = Captcha(session, settings.CAPTCHA_FILE)
c.get(settings.URLS['login_captcha'])
code = raw_input()
print 'check: ', c.check(settings.URLS['check_captcha'], code)

t = Token(session, settings.URL_BASE)
key = t.retrieve_key(settings.URLS['login_token'])
value = t.retrieve_value(key)
print key, value

u = User(session, config.USERNAME, config.PASSWORD, settings.LOGIN_NS, settings.USER_NS)
print 'login: ', u.login(settings.URLS['login'], code, key, value)
ps = u.passengers(settings.URLS['passengers'])

sn = StationName(session, settings.URLS['station_name'], settings.STATION_NAME_FILE)
stations = sn.read()

q = Query(session, settings.URLS['query'], stations, settings.QUERY_ARGS_NS, settings.TRAIN_DATA_JSON_KEY)
res = q.query_once(config.FROM_STATION, config.TO_STATION,
    settings.PURPOSE_CODES[config.TYPE], '2015-04-01', 0)
res = q.filter(res, config.TRAINS, 
    settings.SEAT_CODES.values(), map(lambda s: settings.SEAT_CODES[s], config.SEATS))
print 'lenght of trains: ', len(res)

key = t.retrieve_key(settings.URLS['order_init_token'])
value = t.retrieve_value(key)
print key, value
o = Order(session)
print session.headers
#print o.init(settings.URLS['order_init_submit'], key, value, res[0]['secretStr'],
#    res[0]['date'], settings.PURPOSE_CODES[config.TYPE], config.FROM_STATION, config.TO_STATION)

c.get(settings.URLS['order_captcha'])
code = raw_input()
print 'check: ', c.check(settings.URLS['check_captcha'], code, o.token(settings.URLS['order_confirm']))


if ferr:
    # tear down
    ferr.close()
