#coding=utf-8

import time
import logging

from exception import RetryOutOfTimes

def retry(sleep=1, times=1000):
    def decorator(func):
        def inner(*args, **kwargs):
            for i in range(0, times):
                try:
                    return func(*args, **kwargs)
                except Exception, e:
                    logging.warning('Exception %s occurred, retrying', e)
                time.sleep(sleep)
            raise RetryOutOfTimes(times)
        return inner
    return decorator
