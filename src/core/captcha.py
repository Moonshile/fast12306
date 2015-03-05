#coding=utf-8

from fetch import FetchFile, FetchJson

class Captcha(object):

    def __init__(self, session, captcha_file):
        self.session = session
        self.captcha_file = captcha_file

    def get(self, url):
        FetchFile(self.session).fetch(self.captcha_file, url)

    def check(self, url, code, submit_token=None):
        parameters = [
            ('randCode', code),
            ('rand', 'randp' if submit_token else 'sjrand'),
        ]
        if submit_token:
            parameters.append(('REPEAT_SUBMIT_TOKEN', submit_token))
        assertions = [
            (['status'], True),
        ]
        part = ['data', 'result']
        res = FetchJson(self.session).fetch(url, 
            params=parameters, assertions=assertions, part=part, method='post')
        return res == '1'

