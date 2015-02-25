#coding=utf-8

import requests
import time
import os
import json
import logging

import settings
import config

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d|%(levelname)s|%(message)s',
    datefmt='%Y-%m-%d %X',
    filename=settings.LOGGING_FILE,
)

# decorator to retry if error occured when  perform http requests
def retry(times=100):
    def decorator(func):
        def inner(*args, **kwargs):
            for i in range(0, times):
                try:
                    return func(*args, **kwargs)
                except Exception, e:
                    logging.warning('exception: %s', e)
                    pass
                time.sleep(settings.QUERY_INTERVAL)
            logging.error('retry: retried over %d times in function %s' % (times, func.__name__))
            raise Exception('retry: retried over %d times' % times)
        return inner
    return decorator

