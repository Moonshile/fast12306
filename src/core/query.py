#coding=utf-8

import time

from fetch import FetchJson
from decorators import retry

class Query(object):

    def __init__(self, session, url, station_names, query_args_ns, train_data_json_key):
        self.fj = FetchJson(session)
        self.url = url
        self.sn = station_names
        self.query_args_ns = query_args_ns
        self.tdjk = train_data_json_key
    
    @retry()
    def query_once(self, from_station, to_station, purpose_codes, date, date_priority):
        """

        :param from_station: From station of ticket
        :param to_station: To station of ticket
        :param purpose_codes: Purpose codes of ticket
        :param date: Date of ticket
        :param date_priority: Priority of the date, in fact, it's index of the date in configuration
        """
        
        parameters = [
            (self.query_args_ns + '.train_date', date),
            (self.query_args_ns + '.from_station', self.sn[from_station]),
            (self.query_args_ns + '.to_station', self.sn[to_station]),
            ('purpose_codes', purpose_codes),
        ]
        assertions = [
            (['status'], True),
        ]
        part = ['data']
        cookies = dict(
            _jc_save_fromStation = from_station,
            _jc_save_toStation = to_station,
            _jc_save_fromDate = date,
            _jc_save_toDate = time.strftime('%Y-%m-%d',time.localtime(time.time())),
        )
        trains = self.fj.fetch(self.url, 
            params=parameters, assertions=assertions, part=part, cookies=cookies)
        for t in trains:
            t['date'] = date
            t['date_priority'] = date_priority
        return trains

    def filter(self, trains, op_trains, seats, op_seats):
        """

        :param trains: List of queried trains
        :param op_trains: Optional trains that the user configured
        :param seats: Seat codes that map names of seat type to their codes
        :param op_trains: Optional seat types that the user configured
        """

        op_trains_new = op_trains or map(lambda t: t[self.tdjk]['station_train_code'], trains)
        op_seats_new = op_seats or seats.values()
        def seat_status(t):
            return map(lambda s: t[self.tdjk]['%s_num' % s] not in [u'--', u'无'], op_seats_new)
        res = filter(
            lambda t: any(seat_status(t)) and t[self.tdjk]['station_train_code'] in op_trains_new,
            trains
        )
        for t in res:
            t['seat_priority'] = seat_status(t).index(True)
            t['seat_type'] = op_seats_new[t['seat_priority']]
        def compare_train(x, y):
            if op_seats or x['seat_priority'] == y['seat_priority']:
                if x[self.tdjk]['lishi'] == y[self.tdjk]['lishi']:
                    return 1 if x['date_priority'] > y['date_priority'] else -1
                return 1 if x[self.tdjk]['lishi'] > y[self.tdjk]['lishi'] else -1
            return x['seat_priority'] - y['seat_priority'];
        res.sort(compare_train)
        return res

