#coding=utf-8

import requests
import time
import os
import json
import logging
import re
import subprocess

import settings
import config

from decorators import retry
from captcha import Captcha

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d|%(levelname)s|%(message)s',
    datefmt='%Y-%m-%d %X',
    filename=settings.LOGGING_FILE,
)

class User:

    """
    处理用户登录以及用户信息获取等
    """

    def __init__(self, username, password, session):
        self.username = username
        self.password = password
        self.session = session
        self.base_url = 'https://kyfw.12306.cn'
        self.init_url = 'https://kyfw.12306.cn/otn/login/init'
        self.token_compute_url = 'http://www.goondream.com/qianxi/computekey/'
        self.login_url = 'https://kyfw.12306.cn/otn/login/loginAysnSuggest'
        self.init_pattern = re.compile(r'<script\s+src="(/otn/dynamicJs/.+)"\s+type="text/javascript"\s+xml:space="preserve">\s*</script>\s+</head>')
        self.key_pattern = re.compile(r'function\s+gc\(\)\s*{\s*var\s+key\s*=\s*\'(.+)\'\s*;var\s+value\s*=')
        self.captcha = Captcha(session)
        self.token_key = self.retrieve_token_key()
        self.token_value = self.retrieve_token_value(self.token_key)

    @retry()
    def retrieve_token_key(self):
        res = self.session.get(self.init_url, timeout=settings.TIMEOUT, verify=settings.VERIFY)
        if res.status_code == 200:
            urls = re.findall(self.init_pattern, res.content)
            if len(urls) > 0:
                url = self.base_url + urls[0]
                res = self.session.get(url, timeout=settings.TIMEOUT, verify=settings.VERIFY)
                if res.status_code == 200:
                    keys = re.findall(self.key_pattern, res.content)
                    if len(keys) > 0:
                        return keys[0]
        raise Exception('Fail to retrieve token key when login')

    def retrieve_token_value(self, key):
        with open(settings.CRYPTO_SCRIPT, 'w') as fp:
            with open(settings.CRYPTO_JS, 'r') as rp:
                fp.write(rp.read())
            fp.write('console.info(encode32(bin216(Base32.encrypt(\'1111\', \'%s\'))))\n' % key)
            fp.write('phantom.exit();\n')
        process = subprocess.Popen(
            [settings.PHANTOMJS_PATH, settings.CRYPTO_SCRIPT],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        (stdout, stderr) = process.communicate()
        return stdout.strip()

    @retry(times=4)
    def login(self):
        self.captcha.get()
        code = raw_input(u"输入验证码: ".encode('gbk'))
        while not self.captcha.check(code):
            self.captcha.get()
            code = raw_input(u"输入新的验证码: ".encode('gbk'))
        parameters = [
            (settings.LOGIN_NS + '.user_name', self.username),
            (settings.USER_NS + '.password', self.password),
            ('randCode', code),
            ('randCode_validate', ''),
            (self.token_key, self.token_value),
        ]
        res = self.session.post(self.login_url, params=parameters, timeout=settings.TIMEOUT, verify=settings.VERIFY)
        if res.status_code == 200:
            data = res.json()
            logging.debug(u'loginAysnSuggest return %s' % data)
            return data['status'] and data['data'].get('loginCheck', None) == 'Y'
        raise Exception('Fail to login')
