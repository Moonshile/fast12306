#coding=utf-8

import requests
import time
import os
import json

import settings
import config

from decorators import retry

class StationName:

    """
    获取以及转换车站名称
    """

    def __init__(self, session):
        self.session = session
        self.url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8260'

    @retry()
    def update(self):
        if not os.path.isfile(settings.STATION_NAME_FILE):
            res = self.session.get(self.url, timeout=settings.TIMEOUT, verify=settings.VERIFY)
            assert res.status_code == 200
            with open(settings.STATION_NAME_FILE, 'w') as f:
                f.write(res.content)
        with open(settings.STATION_NAME_FILE, 'r') as f:
            # f.read() get a string like station_names ='..'
            data = f.read().partition('=')[2].strip("'")
            stations = data.split('@')[1:]
            self.data = {}
            for s in stations:
                # s has a format like bjb|北京北|VAP|beijingbei|bjb|0
                items = s.split('|')
                for i in items:
                    self.data[i] = items[2]

    def get(self, key):
        return self.data.get(key, None)
