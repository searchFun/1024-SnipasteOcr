import time
import datetime

default_format = "[%Y%m%d%H%M%S]"


def get_now_time(formatter=default_format):
    return time.strftime(formatter, time.localtime())


def format_time(date, formatter=default_format):
    return date.strftime(formatter.encode('unicode_escape').decode('utf8')).encode('utf-8').decode('unicode_escape')


def get_now_before_time(days=0):
    return datetime.datetime.now() - datetime.timedelta(days=days)


# 获取天数转文字字符串
def get_days_str(days: int):
    if days == 1:
        return '单'
    elif days == 2:
        return '两'
    elif days == 3:
        return '三'
    elif days == 4:
        return '四'
    elif days == 5:
        return '五'
    elif days == 6:
        return '六'
    elif days == 7:
        return '七'
    elif days == 8:
        return '八'
    else:
        raise ValueError("日期太长喽")


# 获取最近天数字符串
def get_recent_date_str(days=1, combine_str=None, formatter=default_format):
    if days == 1:
        return format_time(get_now_before_time(1), formatter)
    else:
        return "%s%s%s" % (format_time(get_now_before_time(days), formatter),
                           combine_str,
                           format_time(get_now_before_time(1), formatter))
