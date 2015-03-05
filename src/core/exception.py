#coding=utf-8

"""
About Exception Level:

1xx: unkown
2xx: fatal, services are not available, must upgrade
3xx: warning, could be omitted and then retried

"""

class BaseException(Exception):

    def __init__(self, info=u'Base Exception of fast12306', level=100):
        super(BaseException, self).__init__('%s\nException level: %d' % (info, level))
        self.level = level





class FatalException(BaseException):

    def __init__(self, info=u'Fatal error occurred', level=200):
        super(FatalException, self).__init__(info, level)

class AssertionsFailedForJson(FatalException):
    
    def __init__(self, keys, value):
        info = u'Assertions for json data failed:\nkeys: %s\nvalue: %s' % (
            unicode(keys), unicode(value)
        )
        super(AssertionsFailedForJson, self).__init__(info, 201)

class HttpContentNoMatches(FatalException):

    def __init__(self, pattern, url, params=None):
        info = u'Can\'t find pattern %s from %s' % (pattern.pattern, url)
        if params:
            info = '%s\n URL parameters: %s' % (info, unicode(params))
        super(HttpContentNoMatches, self).__init__(info, 202)

class RetryOutOfTimes(FatalException):

    def __init__(self, times):
        super(RetryOutOfTimes, self).__init__('Times limit for retrying is %d' % times, 203)





class WarningException(BaseException):

    def __init__(self, info=u'Warning occurred', level=300):
        super(WarningException, self).__init__(info, level)

class HttpStatusNotOK(WarningException):

    def __init__(self, status_code, url, params=None):
        info = u'Got a HTTP code %d for URL %s' % (status_code, url)
        if params:
            info = u'%s\nURL parameters: %s' % (info, unicode(params))
        super(HttpStatusNotOK, self).__init__(info, 301)
