#coding=utf-8

from fetch import FetchJson

class User(object):

    def __init__(self, session, username, password, login_ns, user_ns):
        self.fj = FetchJson(session)
        self.username = username
        self.password = password
        self.login_ns = login_ns
        self.user_ns = user_ns

    def login(self, url, captcha, token_key, token_value):
        parameters = [
            (self.login_ns + '.user_name', self.username),
            (self.user_ns + '.password', self.password),
            ('randCode', captcha),
            ('randCode_validate', ''),
            (token_key, token_value),
        ]
        assertions = [(['status'], True),]
        part = ['data']
        res = self.fj.fetch(url, parameters, 'post', assertions, part)
        return res.get('loginCheck', None) == 'Y'

    def passengers(self, url):
        assertions = [(['status'], True),]
        part = ['data', 'normal_passengers']
        return self.fj.fetch(url, assertions=assertions, part=part)

