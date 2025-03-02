# -*- coding: utf-8 -*-

import datetime
import time
import pytz
import dateutil.relativedelta as drel

utc_0 = int(time.mktime(datetime.datetime(1970, 01, 01).timetuple()))


def get_utc_millis():
    """
    获取系统从1970-1-1至今的utc毫秒数
    :return: 13位毫秒数
    """
    return datetime_to_utc_ms(datetime.datetime.utcnow())


def get_china_time_now():
    """

    获取系统从1970-1-1至今的datetime
    :return:
    """
    return get_china_time_from_ms(get_utc_millis())


def get_china_time_from_ms(ms):
    """
    根据ms获取中国时间
    13位毫秒数 to china datetime
    :param ms: 13位毫秒数
    :return: datetime
    """
    return datetime.datetime.fromtimestamp(
        ms / 1000.0, pytz.timezone('Asia/Shanghai'))


def datetime_to_utc_ms(dt):
    """
    转化为utc的毫秒数
    datetime to 13位毫秒数
    :param dt: datetime
    :return: 13位毫秒数
    """
    return int((time.mktime(dt.utctimetuple()) - utc_0) * 1000) + int(
        dt.microsecond / 1000)


def datetime_to_str(dt, style='%Y-%m-%d %H:%M:%S'):
    """
    datetime to 时间字符串
    :param dt: datetime
    :param style: 需要的时间格式
    :return: 时间字符串
    """
    new_dt = dt.strftime(style)
    return new_dt


def get_after_utc_millis(**kwargs):
    """
    需要操作的时间偏移
    这种写法不支持months，months要使用drel.relativedelta()
    或者直接使用get_after_ms_utc_millis()方法
    minutes=1
    hours=-1
    days=1
    获取系统从1970-1-1至今的再加一段时间后utc毫秒数
    :return: 13位毫秒数
    """
    after_time = datetime.timedelta(**kwargs)
    return datetime_to_utc_ms(datetime.datetime.utcnow() + after_time)


def get_after_ms_utc_millis(ms, **kwargs):
    """
    基于某个13位毫秒数，再便宜一段时间
    获取系统从1970-1-1至今的再加一段时间后utc毫秒数
    :return:
    """
    current = get_china_time_from_ms(ms)
    return datetime_to_utc_ms(current + drel.relativedelta(**kwargs))


def str_to_datetime(str_date, style='%Y-%m-%d %H:%M:%S',
                    tzstr='Asia/Shanghai'):
    """
    style:格式字符串是python的标准日期格式码，例如：
        %Y-%m-%d %H:%M:%S
        %Y-%m-%d
    """
    dt = datetime.datetime.strptime(str_date, style)
    dt = pytz.timezone(tzstr).localize(dt)
    return dt


def str_to_ms(str_date, style='%Y-%m-%d %H:%M:%S', tzstr='Asia/Shanghai'):
    """
    style:格式字符串是python的标准日期格式码，例如：
        %Y-%m-%d %H:%M:%S
        %Y-%m-%d
    """
    dt = datetime.datetime.strptime(str_date, style)
    dt = pytz.timezone(tzstr).localize(dt)
    ms = datetime_to_utc_ms(dt)
    return ms


def get_next_day_from_ms(ms):
    """
    根据当前时间，取之后的一天
    :param ms:
    :return:
    """
    dt = get_china_time_from_ms(ms)
    dt = dt + datetime.timedelta(days=1)
    return datetime_to_utc_ms(dt)


def get_after_x_day_from_ms(ms, days):
    """
    根据当前时间，获取几天后的时间
    :param ms:
    :param days:
    :return:
    """
    dt = get_china_time_from_ms(ms)
    after_time = datetime.timedelta(days=days)
    dt = dt + after_time
    return datetime_to_utc_ms(dt)


def get_day_00_00_00_from_ms(ms):
    """
    根据当前时间，取当天的00：00：00
    :param ms:
    :return:
    """
    dt = get_china_time_from_ms(ms)
    dt_str = datetime_to_str(dt, "%Y-%m-%d")
    return datetime_to_utc_ms(
        str_to_datetime("{} {}".format(dt_str, '00:00:00')))


def get_day_23_59_59_from_ms(ms):
    """
    根据当前时间，取当天的23：59：59
    :param ms:
    :return:
    """
    dt = get_china_time_from_ms(ms)
    dt_str = datetime_to_str(dt, "%Y-%m-%d")
    return datetime_to_utc_ms(
        str_to_datetime("{} {}".format(dt_str, '23:59:59')))


def get_day_12_00_00_from_ms(ms):
    """
    根据当前时间，取当天的12：00：00
    :param ms:
    :return:
    """
    dt = get_china_time_from_ms(ms)
    dt_str = datetime_to_str(dt, "%Y-%m-%d")
    return datetime_to_utc_ms(
        str_to_datetime("{} {}".format(dt_str, '12:00:00')))


def cut_after_min_from_ms(ms):
    """
    把毫秒数的分钟之后的部分cut掉
    :param ms:
    :return:
    """
    dt_china = get_china_time_from_ms(ms)
    # 只取到分钟数
    tmp_dt = datetime.datetime(dt_china.year, dt_china.month, dt_china.day,
                               dt_china.hour, dt_china.minute,
                               tzinfo=dt_china.tzinfo)
    return datetime_to_utc_ms(tmp_dt)


def cut_after_hour_min_second_from_ms(ms):
    """
    把毫秒数的时分秒后的部分cut掉
    :param ms:
    :return:
    """
    dt_china = get_china_time_from_ms(ms)

    tmp_dt = datetime.datetime(dt_china.year, dt_china.month, dt_china.day,
                               tzinfo=dt_china.tzinfo)
    return datetime_to_utc_ms(tmp_dt)


def get_first_day_of_month_from_ms(ms):
    """
    把毫秒数的时分秒后的部分cut掉
    :param ms:
    :return:
    """
    dt_china = get_china_time_from_ms(ms)

    tmp_dt = datetime.datetime(dt_china.year, dt_china.month, 1,
                               tzinfo=dt_china.tzinfo)
    return datetime_to_utc_ms(tmp_dt)


def if_two_ms_in_one_week(ms1, ms2):
    """
    两个时间是否在同一周
    :param ms1:
    :param ms2:
    :return:
    """

    dt1 = get_china_time_from_ms(ms1)
    dt2 = get_china_time_from_ms(ms2)

    dt1_year = dt1.year
    dt2_year = dt2.year

    dt1_week = dt1.isocalendar()[1]
    dt2_week = dt2.isocalendar()[1]

    if dt1_year == dt2_year and dt1_week == dt2_week:
        return True
    return False


def ms_to_str(ms, style='%Y-%m-%d %H:%M:%S'):
    """
    ms 转时间字符串
    :param ms:
    :param style:
    :return:
    """
    dt = get_china_time_from_ms(ms)
    return datetime_to_str(dt, style=style)


def is_overlapping_hours_list(hours_list):
    """
    判断时间列表是否重叠
    :param hours_list: ["09:00-12:00", "13:00-18:00"]
    :return:
    """
    if not hours_list:
        return False

    duration_list = hours_list

    need_insert_list = []
    for duration in duration_list:
        if len(duration) != 11:
            return False
        hour_st_et_list = duration.split("-")
        hour_st = hour_st_et_list[0]
        hour_et = hour_st_et_list[1]
        hour_st_int = int(hour_st.replace(":", ""))
        hour_et_int = int(hour_et.replace(":", ""))
        if not 0 <= hour_st_int < hour_et_int <= 2400:
            return False
        need_insert_list.append(
            {"hour_b_str": hour_st, "hour_b_int": hour_st_int,
             "hour_e_str": hour_et, "hour_e_int": hour_et_int}
        )

    # 判断当前要插入的数据，时间两两不重叠
    for doc1 in need_insert_list:
        for doc2 in need_insert_list:
            if doc1 == doc2:
                continue
            t_b1 = doc1["hour_b_int"]
            t_e1 = doc1["hour_e_int"]
            t_b2 = doc2["hour_b_int"]
            t_e2 = doc2["hour_e_int"]
            if not (t_e2 <= t_b1 or t_b2 >= t_e1):
                return False
    return need_insert_list


def get_week_day_number(ms):
    """
    获取周几
    :param ms:
    :return:
    """
    dt = get_china_time_from_ms(ms)
    return dt.weekday() + 1


if __name__ == '__main__':
    """"""
