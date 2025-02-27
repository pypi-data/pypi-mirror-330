# -*- coding: utf-8 -*-
import datetime

from chaokai.common.uid import fmt_time


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
