# -*- coding: utf-8 -*-
import datetime
import time


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


def excel_to_timestamp(excel_date):
    # Excel的基准日期是1899年12月30日，但由于1900年的错误，我们通常从1899年12月31日开始计算
    excel_base_date = datetime.datetime(1899, 12, 31)
    # 由于Excel日期是从0开始的（相对于基准日期的整数部分），我们需要加上一天（转换为天数）
    days_since_base = int(excel_date)
    delta = datetime.timedelta(days=days_since_base)
    normal_date = excel_base_date + delta
    # 将datetime对象转换为时间戳（注意：这是本地时间的时间戳）
    timestamp = normal_date.timestamp()
    return int(timestamp)


if __name__ == '__main__':
    r = excel_to_timestamp(43665)
    print(r)
