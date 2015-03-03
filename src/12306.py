#coding=utf-8

import requests
import json
import sys
import logging

import config

from core import settings, Query

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d|%(levelname)s|%(message)s',
    datefmt='%Y-%m-%d %X',
    filename=settings.LOGGING_FILE,
)

# redirect stderr to settings.ERR_LOG_FILE
ferr = open(settings.ERR_LOG_FILE, 'w')
sys.stderr = ferr

session = requests.Session()
session.timeout = settings.TIMEOUT
session.verify = settings.VERIFY
q = Query(session, settings.URLS['query'], settings.QUERY_ARGS_NS, settings.TRAIN_DATA_JSON_KEY)
res = q.query_once('XFN', 'BXP', 'ADULT', '2015-04-01', 0)
print map(lambda t: t['queryLeftNewDTO']['station_train_code'], 
    q.filter(res, config.TRAINS, settings.SEAT_CODES.values, map(lambda s: settings.SEAT_CODES[s], config.SEATS)))

# tear down
ferr.close()
