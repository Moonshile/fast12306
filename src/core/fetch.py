#coding=utf-8

import re
import logging

from requests import Session
from exception import AssertionsFailedForJson, HttpContentNoMatches, HttpStatusNotOK

class FetchBase(object):

    def __init__(self, session):
        super(FetchBase, self).__init__()
        self.session = session
        self.methods = {
            'get': self.session.get,
            'post': self.session.post,
        }


class FetchJson(FetchBase):

    def __init__(self, session):
        super(FetchJson, self).__init__(session)

    def assert_dict(self, dict_data, assertions):
        for (keys, value) in assertions:
            actual = reduce(lambda res, k: res[k], keys, dict_data)
            if actual != value:
                raise AssertionsFailedForJson(keys, value)

    def fetch(self, url, params=None, method='get', assertions=[], part=[]):
        """

        :param url: URL to fetch json data
        :param params: Query parameters for the URL
        :param method: Method of http request
        :param assertions: Infomation to assert the fetched data, has a format `[(keys, value),]`
        :param part: The part of the fetched json data which should be returned
        """

        r = self.methods[method](url, params=params)
        logging.debug(r.content)
        if r.status_code == 200:
            json_data = r.json()
            self.assert_dict(json_data, assertions)
            return reduce(lambda res, k: res[k], part, json_data) if part else json_data
        raise HttpStatusNotOK(r.status_code, url, params)


class FetchFile(FetchBase):

    def __init__(self, session):
        super(FetchFile, self).__init__(session)

    def fetch(self, filename, url, params=None, method='get', func=None):
        """

        :param filename: The file to store the fetched data
        :param url: URL to fetch data
        :param params: Query parameters for the URL
        :param method: Method of http request
        :param func: Function to do preprocess for the fetched data
        """

        r = self.methods[method](url, params=params)
        logging.debug(r.content)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(func(r.content) if func else r.content)
        raise HttpStatusNotOK(r.status_code, url, params)


class FetchSlice(FetchBase):

    def __init__(self, session):
        super(FetchSlice, self).__init__(session)

    def fetch(self, pattern, url, params=None, method='get'):
        r = self.methods[method](url, params=params)
        logging.debug(r.content)
        if r.status_code == 200:
            matches = re.findall(pattern, r.content)
            if len(matches) > 0:
                return matches
            raise HttpContentNoMatches(pattern, url, params)
        raise HttpStatusNotOK(r.status_code, url, params)
