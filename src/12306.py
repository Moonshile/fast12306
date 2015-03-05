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

sn = StationName(session, settings.URLS['station_name'], settings.STATION_NAME_FILE)
stations = sn.read()

def query_do():
    q = Query(session, settings.URLS['query'], stations, settings.QUERY_ARGS_NS, settings.TRAIN_DATA_JSON_KEY)
    i = 0
    while True:
        trains = q.query_once(config.FROM_STATION, config.TO_STATION,
            settings.PURPOSE_CODES[config.TYPE], config.TRAIN_DATE[i], i)
        if trains:
            filtered = q.filter(trains, config.TRAINS, 
                settings.SEAT_CODES.values(), map(lambda s: settings.SEAT_CODES[s], config.SEATS))
            if filtered:
                print '\x07'
            print map(
                lambda t: '%s %s %s' % (
                    t[settings.TRAIN_DATA_JSON_KEY]['station_train_code'],
                    t['date'],
                    t['seat_type']
                ),
                filtered
            )
            i = (i + 1)%len(config.TRAIN_DATE)
        time.sleep(settings.QUERY_INTERVAL)

query_do()

"""

# work
uname = raw_input('输入12306账户名： ')
pwd = raw_input('输入密码： ')
print uname, pwd

c = Captcha(session, settings.CAPTCHA_FILE)
print c.get(settings.URLS['login_captcha'])
code = raw_input('验证码： ')
print 'check: ', c.check(settings.URLS['check_captcha'], code)

t = Token(session, settings.URL_BASE)
key = t.retrieve_key(settings.URLS['login_token'])
value = t.retrieve_value(key)
print key, value

u = User(session, uname, pwd, settings.LOGIN_NS, settings.USER_NS)
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
print o.init(settings.URLS['order_init_submit'], key, value, res[0]['secretStr'],
    res[0]['date'], settings.PURPOSE_CODES[config.TYPE], config.FROM_STATION, config.TO_STATION)

submit_token = o.submit_token(settings.URLS['order_confirm'])

c.get(settings.URLS['order_captcha'])
code = raw_input()
print 'check: ', c.check(settings.URLS['check_captcha'], code, submit_token)

print 'check order: ', o.check(
    url=settings.URLS['order_check'],
    seat_type=settings.SEAT_ID[res[0]['seat_type']],
    ticket_type=settings.PURPOSE_ID[config.TYPE],
    passenger_name=config.PASSENGERS[0][0],
    id_card=config.PASSENGERS[0][1],
    phone=config.PASSENGERS[0][2],
    captcha=code,
    token_key=key,
    token_value=value,
    submit_token=submit_token,
)

"""

if ferr:
    # tear down
    ferr.close()
