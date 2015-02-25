#coding=utf-8

import os

if not os.path.isdir('log'):
    os.mkdir('log')

import requests
import time
import json
import sys

import settings
import config

from query import Query
from user import User

# 错误信息输出到err.log中
ferr = open(settings.ERR_LOG_FILE, 'w')
sys.stderr = ferr

# 开始工作！
session = requests.Session()

# query = Query(session)
# query.do()

user = User(config.USERNAME, config.PASSWORD, session)

# 收尾工作
ferr.close()

