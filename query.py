#coding=utf-8

import requests
import time
import os
import json

import settings
import config

from station_name import StationName
from decorators import retry

class Query:

    """
    查询余票信息
    """

    def __init__(self, session):
        self.session = session
        self.url = 'https://kyfw.12306.cn/otn/leftTicket/queryT'
        self.seats = []
        for s in config.SEATS:
            code = settings.SEAT_CODES.get(s, None)
            if code:
                self.seats.append(code)
            else:
                print u'座位 %s 设置错误，请修改' % s
        if len(config.SEATS) == 0:
            self.seats = settings.SEAT_CODES.values()

        # 更新车站名称信息
        self.stations = StationName(session)
        self.stations.update()

    @retry()
    def query_once(self, date, from_station, to_station, purpose_codes):
        parameters = [
            (settings.QUERY_ARGS_NS + '.train_date', date),
            (settings.QUERY_ARGS_NS + '.from_station', from_station),
            (settings.QUERY_ARGS_NS + '.to_station', to_station),
            ('purpose_codes', purpose_codes),
        ]
        res = self.session.get(self.url, params=parameters, timeout=settings.TIMEOUT, verify=settings.VERIFY)
        if res.status_code == 200:
            try:
                #print res.content
                self.trains = res.json()[u'data']
                for t in self.trains:
                    t['date'] = date
                return True
            except:
                return False
        elif res.status_code == 403:
            print u'孩子你被禁止访问12306了，把查询间隔改大一些，十分钟后再来刷刷刷'
        return False

    # 筛出候选车次
    def optional(self):
        self.options = filter(
            lambda t: any(map(
                lambda s: t['queryLeftNewDTO']['%s_num' % s] not in [u'--', u'无'],
                self.seats
            )) and (len(config.TRAINS) == 0 or t['queryLeftNewDTO']['station_train_code'] in config.TRAINS),
            self.trains
        )
        def find(t):
            for i in range(0, len(self.seats)):
                if t['queryLeftNewDTO']['%s_num' % self.seats[i]] not in [u'--', u'无']:
                    t['seat_type'] = self.seats[i]
                    return i
            return 10000
        def compare_train(x, y):
            xi = find(x)
            yi = find(y)
            if len(config.SEATS) == 0 or xi == yi:
                return 1 if x['queryLeftNewDTO']['lishi'] > y['queryLeftNewDTO']['lishi'] else -1
            return xi - yi;
        # ensure that every train has set attribute 'seat_type'
        for t in self.options:
            find(t)
        self.options.sort(compare_train)
        return True if len(self.options) > 0 else False

    def do(self):
        i = 0
        fs = self.stations.get(config.FROM_STATION)
        ts = self.stations.get(config.TO_STATION)
        if not fs:
            print u'出发车站 %s 名称配置错误，请修改' % config.FROM_STATION
            return False
        if not ts:
            print u'目的车站 %s 名称配置错误，请修改' % config.TO_STATION
            return False
        while True:
            if self.query_once(config.TRAIN_DATE[i], fs, ts, settings.PURPOSE_CODES[config.TYPE]):
                if self.optional():
                    print '\x07'
                print map(lambda t: '%s %s %s' % (
                    t['queryLeftNewDTO']['station_train_code'],
                    t['date'],
                    t['seat_type'],
                ), self.options)
                # inc i only if query successfully
                i = (i + 1)%len(config.TRAIN_DATE)
                
            time.sleep(settings.QUERY_INTERVAL)
        return True
