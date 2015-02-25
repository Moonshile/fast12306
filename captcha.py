#coding=utf-8

import requests
import time
import os
import json

import settings
import config

from decorators import retry

class Captcha:

    """
    获取和校验验证码
    """

    def __init__(self, session):
        self.session = session
        self.get_url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand'
        self.check_url = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'

    @retry()
    def get(self):
        res = self.session.get(self.get_url, timeout=settings.TIMEOUT, verify=settings.VERIFY)
        if res.status_code == 200:
            with open(settings.CAPTCHA_FILE, 'wb') as fp:
                fp.write(res.content)
        else:
            raise Exception('Fail to get Captcha')

    @retry()
    def check(self, code):
        parameters = [
            ('randCode', code),
            ('rand', 'sjrand'),
        ]
        res = self.session.post(self.check_url, params=parameters, timeout=settings.TIMEOUT, verify=settings.VERIFY)
        if res.status_code == 200:
            data = res.json()
            return  data['status'] and data['data']['result'] == '1'
        raise Exception('Fail to check Captcha')
