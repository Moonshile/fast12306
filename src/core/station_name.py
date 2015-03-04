#coding=utf-8

import os
from fetch import FetchFile

class StationName(object):

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
        FetchFile(self.session).fetch(self.station_name_file, self.url,
            func=lambda x: x.partition('=')[2].strip("'"))
