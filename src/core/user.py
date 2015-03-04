#coding=utf-8

class User(object):

    def __init__(self, session, username, password):
        self.session = session
        self.username = username
        self.password = password
