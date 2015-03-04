#coding=utf-8

import re

from fetch import FetchSlice

class Token(object):

    def __init__(self, session):
        self.session = session
        self.init_url_pattern = re.compile(r'<script\s+src="/(otn/dynamicJs/.+)"\s+type="text/javascript"\s+xml:space="preserve">\s*</script>\s+</head>')
        self.key_pattern = re.compile(r'function\s+gc\(\)\s*{\s*var\s+key\s*=\s*\'(.+)\'\s*;var\s+value\s*=')
        

    def retrieve_key(self, init_url, base_url):
        """

        :param init_url: URL which contains the link to the js file that contains the token key
        :param base_url: URL base
        """

        fs = FetchSlice(self.session)
        url = fs.fetch(self.init_url_pattern, init_url)[0]
        key = fs.fetch(self.key_pattern, base_url + url)[0]
        return key

    def retrieve_value(self, key):
        return self.encode32(self.bin216(self.base32('1111', key)))

    """
    The following methods are translated from a javascript file from 12306
    """


    def text2array(self, text, include_length):
        length = len(text)
        res = []
        for i in range(0, length, 4):
            res.append(ord(text[i]) | ord(text[i + 1]) << 8 | ord(text[i + 2]) << 16 | ord(text[i + 3]) << 24)
        if include_length:
            res.append(length)
        return res

    def array2text(self, data, include_length):
        """
        length = len(data)
        n = (length - 1) << 2;
        if include_length:
            m = data[length - 1]
            if m < n - 3 or m > n:
                return None
            n = m
        res = reduce(
            lambda res, x: res + x,
            map(
                lambda x: chr(x & 0xff) + chr(x >> 8 & 0xff) + chr(x >> 16 & 0xff) + chr(x >> 24 & 0xff),
                data
            ),
            ''
        )
        if include_length:
            return res[:n]
        else:
            return res
        """
        return map(lambda x: ((x&0xff)<<24)|((x>>8&0xff)<<16)|((x>>16&0xff)<<8)|(x>>24&0xff), data)

    def base32(self, text, key):
        delta = 0x9E3779B8
        def rshift(v, n):
            return (v % 0x100000000) >> n
        def compute_mx(z, y, s, k, p, e):
            r1 = rshift(z, 5)
            r2 = y << 2 & 0xffffffff
            r3 =  r1 ^ r2
            r4 = rshift(y, 3)
            r5 = z << 4 & 0xffffffff
            r6 = r4 ^ r5
            r7 = r3 + r6 & 0xffffffff
            r8 = s ^ y
            r9 = k[p & 3 ^ e] ^ z
            r10 = r8 + r9 & 0xffffffff
            return r7 ^ r10
        if text == '':
            return ''
        v = self.text2array(text, True)
        k = self.text2array(key, False)
        if len(k) < 4:
            for i in range(0, 4 - len(k)):
                k.append(0)
        n = len(v) - 1
        z = v[n]
        y = v[0]
        mx = None
        e = None
        p = None
        q = int(6 + 52/(n + 1))
        s = 0
        while 0 < q:
            q = q - 1
            s = (s + delta & 0xffffffff)
            e = rshift(s, 2) & 3
            for p in range(0, n):
                y = v[p + 1]
                mx = compute_mx(z, y, s, k, p, e)
                z = v[p] = (v[p] + mx & 0xffffffff)
            p = n
            y = v[0]
            mx = compute_mx(z, y, s, k, p, e)
            z = v[n] = (v[n] + mx & 0xffffffff)
        return self.array2text(v, False)

    def bin216(self, text):
        """
        i = None
        o = ''
        n = None
        text = text + ''
        l = len(text)
        b = ''
        for i in range(0, l):
            b = ord(text[i])
            n = hex(b).replace('0x', '')
            o = o + ('0' + n if len(n) < 2 else n)
        return o
        """
        return reduce(lambda res, x: res + x,
            map(
                lambda x: hex(0x100000000 | x)[3:],
                text
            ),
            ''
        )

    def encode32(self, text):
        keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        output = ''
        chr1 = None
        chr2 = None
        chr3 = ''
        enc1 = None
        enc2 = None
        enc3 = None
        enc4 = ''
        i = 0
        while True:
            chr1 = ord(text[i])
            i = i + 1
            chr2 = ord(text[i]) if i < len(text) else None
            i = i + 1
            chr3 = ord(text[i]) if i < len(text) else None
            i = i + 1
            enc1 = chr1 >> 2
            enc2 = ((chr1 & 3) << 4) | ((chr2 >> 4) if chr2 else 0)
            enc3 = (((chr2 & 15) << 2) if chr2 else 0) | ((chr3 >> 6) if chr3 else 0)
            enc4 = chr3 & 63 if chr3 else 0
            if chr2 is None:
                enc3 = enc4 = 64
            elif chr3 is None:
                enc4 = 64
            output = output + keyStr[enc1] + keyStr[enc2] + keyStr[enc3] + keyStr[enc4]
            chr1 = chr2 = chr3 = ''
            enc1 = enc2 = enc3 = enc4 = ''
            if i >= len(text):
                break
        return output
