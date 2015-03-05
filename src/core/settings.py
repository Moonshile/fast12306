#coding=utf-8

import os

# Basic settings

# requests settings
TIMEOUT = 5
VERIFY = False

# directories might be used
LOCATIONS = {
    'log': 'log',
    'data': 'data',
}

# stderr is redirected to this file
ERR_LOG_FILE = os.path.join(LOCATIONS['log'], 'err.log')
# log in this file
LOGGING_FILE = os.path.join(LOCATIONS['log'], 'requests.log')

STATION_NAME_FILE = os.path.join(LOCATIONS['data'], 'station_name.js')
CAPTCHA_FILE = os.path.join(LOCATIONS['data'], 'captcha.png')
CRYPTO_JS = os.path.join(LOCATIONS['data'], 'crypto.js')
CRYPTO_SCRIPT = os.path.join(LOCATIONS['data'], 'do_crypto.js')

# Query settings

QUERY_INTERVAL = 1
QUERY_ARGS_NS = 'leftTicketDTO'
TRAIN_DATA_JSON_KEY = 'queryLeftNewDTO'

LOGIN_NS = 'loginUserDTO'
USER_NS = 'userDTO'

PURPOSE_CODES = {'学生': '0X00', '普通': 'ADULT'}
PURPOSE_ID = {'0X00': 3, '学生': 3, 'ADULT': 1, '普通': 1}
SEAT_CODES = {
    '商务座': 'swz',
    '特等座': 'tz',
    '一等座': 'zy',
    '二等座': 'ze',
    '高级软卧': 'gr',
    '软卧': 'rw',
    '硬卧': 'yw',
    '软座': 'rz',
    '硬座': 'yz',
    '无座': 'wz',
    '其他': 'qt',
}
SEAT_ID = {
    'SWZ': '9',
    'TZ': 'P',
    'ZY': 'M',
    'ZE': 'O',
    'GR': '6',
    'RW': '4',
    'YW': '3',
    'RZ': '2',
    'YZ': '1',
    'WZ': 'WZ',
    'QT': '',
}

URL_BASE = 'https://kyfw.12306.cn/'

URLS = {
    'entry': URL_BASE + 'otn/',
    'station_name': URL_BASE + 'otn/resources/js/framework/station_name.js?station_version=1.8260',
    'query': URL_BASE + 'otn/leftTicket/queryT',
    'query_log': URL_BASE + 'otn/leftTicket/log',
    'login_captcha': URL_BASE + 'otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand',
    'order_captcha': URL_BASE + 'otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp',
    'check_captcha': URL_BASE + 'otn/passcodeNew/checkRandCodeAnsyn',
    'login_token': URL_BASE + 'otn/login/init',
    'order_init_token': URL_BASE + 'otn/leftTicket/init',
    'login': URL_BASE + 'otn/login/loginAysnSuggest',
    'check_login': URL_BASE + 'otn/login/checkUser',
    'passengers': URL_BASE + 'otn/confirmPassenger/getPassengerDTOs',
    'order_init_submit': URL_BASE + 'otn/leftTicket/submitOrderRequest',
    'order_confirm': URL_BASE + 'otn/confirmPassenger/initDc',
    'order_check': URL_BASE + 'otn/confirmPassenger/checkOrderInfo',
}

# 3rd party tools settings

# Setup for settings

import socket

if socket.gethostname() in ['duankq-ThinkPad-X201', ]:
    DEBUG = True
else:
    DEBUG = False

import os

for loc in LOCATIONS.values():
    if not os.path.isdir(loc):
        os.mkdir(loc)

for (k, v) in SEAT_CODES.iteritems():
    SEAT_ID[k] = SEAT_ID[v.upper()]
    SEAT_ID[v] = SEAT_ID[v.upper()]
