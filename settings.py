#coding=utf-8

# Basic settings
TIMEOUT = 5
VERIFY = False
STATION_NAME_FILE = 'station_name.js'
ERR_LOG_FILE = 'err.log'
LOGGING_FILE = 'requests.log'
CAPTCHA_FILE = 'captcha.png'
CRYPTO_JS = 'crypto.js' # 可恶的12306弄了一个很复杂的键值算法，全放这里了
CRYPTO_SCRIPT = 'do_crypto.js'

# Query settings
QUERY_INTERVAL = 1
QUERY_ARGS_NS = 'leftTicketDTO'

LOGIN_NS = 'loginUserDTO'
USER_NS = 'userDTO'

PURPOSE_CODES = {'学生': '0X00', '普通': 'ADULT'}
SEAT_CODES = {
    '商务座': 'swz',
    '特等座': 'tz',
    '一等座': 'zy',
    '二等座': 'ze',
    '高级软卧': 'gr',
    '软卧': 'rw',
    '硬卧': 'yw',
    '软座': 'rz',
    '硬座': 'yz',
    '无座': 'wz',
    '其他': 'qt',
}

# 3rd party tools settings
PHANTOMJS_PATH = 'phantomjs-2.0.0-windows/bin/phantomjs.exe'