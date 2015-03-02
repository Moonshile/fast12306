#coding=utf-8

import requests
import time
import os
import json
import logging
import re
import subprocess

import settings
import config

from decorators import retry
from captcha import Captcha

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d|%(levelname)s|%(message)s',
    datefmt='%Y-%m-%d %X',
    filename=settings.LOGGING_FILE,
)

class Order:

    def __init__(self, session):
        self.session = session
        self.submit_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
