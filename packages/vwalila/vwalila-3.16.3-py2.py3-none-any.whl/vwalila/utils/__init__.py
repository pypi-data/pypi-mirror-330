# -*- coding: utf-8 -*-

import time
import datetime
import pytz

utc_0 = int(time.mktime(datetime.datetime(1970, 01, 01).timetuple()))


def get_utc_millis():
    """

    获取系统从1970-1-1至今的utc毫秒数
    :return:
    """
    return datetime_to_utc_ms(datetime.datetime.utcnow())


def datetime_to_utc_ms(dt):
    """
    转化为utc的毫秒数
    :param dt:
    :return:
    """
    return int((time.mktime(dt.utctimetuple()) - utc_0) * 1000) + \
        int(dt.microsecond / 1000)


def dt_ms_to_str(dt_ms, style='%Y-%m-%d %H:%M:%S'):
    """
    :param dt_ms:
    :param style:
    :return:
    """
    dt = get_china_time_from_ms(dt_ms)
    new_dt = dt.strftime(style)
    return new_dt


def get_china_time_from_ms(ms):
    """
    获取中国时间
    :param ms:
    :return:
    """
    return datetime.datetime.fromtimestamp(
        ms / 1000.0, pytz.timezone('Asia/Shanghai'))


