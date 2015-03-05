#coding=utf-8

import time
import re

from fetch import FetchJson, FetchSlice
from decorators import retry

class Order(object):

    def __init__(self, session):
        self.fj = FetchJson(session)
        self.fs = FetchSlice(session)
        self.token_pattern = re.compile(r'globalRepeatSubmitToken\s+=\s+\'(.+)\'')

    def init(self, url, token_key, token_value, secret_str,
        train_date, purpose_codes, from_station_name, to_station_name):
        parameters = [
            (token_key, token_value),
            ('myversion', 'undefined'),
            ('secretStr', secret_str),
            ('train_date', train_date),
            ('back_train_date', time.strftime('%Y-%m-%d',time.localtime(time.time()))),
            ('tour_flag', 'dc'),
            ('purpose_codes', purpose_codes),
            ('query_from_station_name', from_station_name),
            ('query_to_station_name', to_station_name),
            ('undefined', ''),
        ]
        assertions = [(['status'], True),]
        part = ['data']
        return self.fj.fetch(url, parameters, 'post', assertions, part)

    def token(self, url):
        return self.fs.fetch(self.token_pattern, url)[0]
