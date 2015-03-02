#coding=utf-8

import requests
import json
import sys

from core import StationName, settings

# redirect stderr to settings.ERR_LOG_FILE
ferr = open(settings.ERR_LOG_FILE, 'w')
sys.stderr = ferr

session = requests.Session()
session.timeout = settings.TIMEOUT
session.verify = settings.VERIFY

sn = StationName(session, settings.URLS['station_name'], settings.STATION_NAME_FILE)
sn.read()

# tear down
ferr.close()
