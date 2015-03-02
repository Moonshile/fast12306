#coding=utf-8

from StationName import ensure_has_stations

class Query:

    def __init__(self, session, url, query_args_ns, train_data_json_key):
        self.session = session
        self.url = url
        self.query_args_ns = query_args_ns
        self.tdjk = train_data_json_key

    def query_once(self, from_station, to_station, purpose_codes, date, date_priority):
        parameters = [
            (self.query_args_ns + '.train_date', date),
            (self.query_args_ns + '.from_station', from_station),
            (self.query_args_ns + '.to_station', to_station),
            ('purpose_codes', purpose_codes),
        ]
        res = self.session.get(self.url, params=parameters, timeout=settings.TIMEOUT, verify=settings.VERIFY)
        assert res.status_code == 200
        d = res.json()
        assert d['status']
        trains = d['data']
        for t in trains:
            t['date'] = date
            t['date_priority'] = date_priority
        return trains

    def filter(self, trains, op_trains, seats, op_seats):
        op_trains_new = op_trains or map(lambda t: t[self.tdjk]['station_train_code'], trains)
        op_seats_new = op_seats or seats.values()
        def seat_status(t):
            return map(lambda s: t[self.tdjk]['%s_num' % s] not in [u'--', u'无'], op_seats_new)
        res = filter(
            lambda t: any(seat_status(t)) and t[self.tdjk]['station_train_code'] in op_trains_new,
            self.trains
        )
        for t in res:
            t['seat_priority'] = seat_status(t).index(True)
            t['seat_type'] = op_seats_new[t['seat_priority']]
        def compare_train(x, y):
            xi = find(x)
            yi = find(y)
            if op_seats or x['seat_priority'] == y['seat_priority']:
                if x[self.tdjk]['lishi'] == y[self.tdjk]['lishi']:
                    return 1 if x['date_priority'] > y['date_priority'] else -1
                return 1 if x[self.tdjk]['lishi'] > y[self.tdjk]['lishi'] else -1
            return x['seat_priority'] - y['seat_priority'];
        res.sort(compare_train)
        return res

