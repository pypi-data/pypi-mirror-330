# -*- coding: utf-8 -*-
import datetime
import time
import uuid


def create_uuid(first_str='', length=10, is_upper=False):
    """
    生成uuid
    """
    uuid4 = str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '')
    resp_str = str(first_str) + uuid4[:length]

    if is_upper:
        resp_str = resp_str.upper()

    return resp_str


def create_date_id(prefix='', suffix=''):
    """

    :param length: 长充
    :param prefix: 前缀
    :param suffix: 后缀
    :return: 20位时间ID
    """
    """
    生成基于时间的数字id
    """
    date_str = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))

    return prefix + date_str + suffix


def fmt_time(timestamp, status=1):
    """格式化时间戳"""
    try:
        tsp = int(timestamp)
    except:
        return ''

    if tsp == 0:
        return ''

    try:
        if status == 1:
            date = time.strftime('%Y.%m.%d %H:%M', time.localtime(tsp))
        elif status == 2:
            date = time.strftime('%Y.%m.%d', time.localtime(tsp))
        elif status == 3:
            date = time.strftime('%Y/%m/%d', time.localtime(tsp))
        elif status == 4:
            date = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(tsp))
        elif status == 5:
            date = time.strftime('%Y-%m', time.localtime(tsp))
        elif status == 6:
            date = time.strftime('%Y%m%d', time.localtime(tsp))
        elif status == 7:
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tsp))
        elif status == 8:
            date = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(tsp))
        elif status == 9:
            date = time.strftime('%Y-%m-%d', time.localtime(tsp))
        else:
            date = time.strftime('%Y.%m.%d', time.localtime(tsp))
    except:
        return '0'

    return date


if __name__ == '__main__':
    r = create_uuid()
    print(len(r), '--', r)

    r = create_date_id()
    print(r, len(r))

