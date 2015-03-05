#coding=utf-8

from fetch import FetchFile, FetchJson

class Captcha(object):

    def __init__(self, session, captcha_file):
        self.session = session
        self.captcha_file = captcha_file

    def get(self, url):
        FetchFile(self.session).fetch(self.captcha_file, url)

    def check(self, url, code, repeat_submit_token=None):
        parameters = [
            ('randCode', code),
            ('rand', 'randp' if repeat_submit_token else 'sjrand'),
        ]
        if repeat_submit_token:
            parameters.append(('REPEAT_SUBMIT_TOKEN', repeat_submit_token))
        assertions = [
            (['status'], True),
        ]
        part = ['data', 'result']
        res = FetchJson(self.session).fetch(url, 
            params=parameters, assertions=assertions, part=part, method='post')
        return res == '1'

