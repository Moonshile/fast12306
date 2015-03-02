#coding=utf-8

import os

class StationName:

    def __init__(self, session, url, station_name_file):
        self.session = session
        self.url = url
        self.station_name_file = station_name_file

    def read(self):
        if not os.path.isfile(self.station_name_file):
            self.update()
        with open(self.station_name_file, 'r') as f:
            # f.read() get a string like '@bjb|北京北|VAP|beijingbei|bjb|0...'
            station_str = f.read()
            stations = station_str.split('@')[1:]
            data = {}
            for s in stations:
                # s has a format like bjb|北京北|VAP|beijingbei|bjb|0
                items = s.split('|')
                for i in items:
                    data[i] = items[2]
        self.data = data
        return data

    def update(self):
        res = self.session.get(self.url)
        assert res.status_code == 200
        with open(self.station_name_file, 'w') as f:
            f.write(res.content.partition('=')[2].strip("'"))

    # decorator to ensure has stations saved
    def ensure_has_stations(sn):
        def decorator(funcs):
            def inner(*args, **kwargs):
                if not os.path.isfile(sn.station_name_file):
                    sn.update()
                return funcs(*args, **kwargs)
            return inner
        return decorator
