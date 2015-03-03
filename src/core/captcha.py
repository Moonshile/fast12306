#coding=utf-8

from fetch import FetchFile, FetchJson

class Captcha(object):

    def __init__(self, session, captcha_file):
        self.session = session
        self.captcha_file = captcha_file

    def get(self, url):
        FetchFile(self.session).fetch(self.captcha_file, url)

    def check(self, url, code):
        parameters = [
            ('randCode', code),
            ('rand', 'sjrand'),
        ]
        assertions = [
            (['status'], True),
        ]
        part = ['data', 'result']
        res = FetchJson(self.session).fetch(url, 
            params=parameters, assertions=assertions, part=part, method='post')
        return res == '1'

