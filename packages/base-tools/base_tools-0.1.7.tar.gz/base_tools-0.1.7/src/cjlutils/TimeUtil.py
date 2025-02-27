import datetime
import time
from enum import Enum

# 下面给出每个时间单位内有多少微妙，方便转换

# 微妙
MICROSECOND_PER_MICRO = 1
# 毫秒
MILLISECOND_PER_MICRO = MICROSECOND_PER_MICRO * 1000
# 秒
SECOND_PER_MICRO = MILLISECOND_PER_MICRO * 1000
# 分钟
MINUTE_PER_MICRO = SECOND_PER_MICRO * 60
# 小时
HOUR_PER_MICRO = MINUTE_PER_MICRO * 60
# 天
DAY_PER_MICRO = HOUR_PER_MICRO * 24
# 周
WEAK_PER_MICRO = DAY_PER_MICRO * 7


class TimeUnitEnum(Enum):
    MICROSECOND = MICROSECOND_PER_MICRO,
    MILLISECOND = MILLISECOND_PER_MICRO,
    SECOND = SECOND_PER_MICRO,
    MINUTE = MINUTE_PER_MICRO,
    HOUR = HOUR_PER_MICRO,
    DAY = DAY_PER_MICRO,
    WEAK = WEAK_PER_MICRO,


def get_timestamp(unit: TimeUnitEnum = TimeUnitEnum.SECOND) -> float:
    """
    获取时间戳
    :param unit: 时间单位单位，默认秒级
    :return: 指定时间单位的时间戳
    """
    return time.time() * TimeUnitEnum.SECOND.value[0] / unit.value[0]


def get_date_str(timestamp: float, hours=0) -> str:
    '''
    获取日期时间字符串
    :param timestamp: 秒级时间戳
    :param hours: 时区便宜，默认东8区
    :return:
    '''
    date = datetime.datetime.fromtimestamp(timestamp)
    beijing_date = date + datetime.timedelta(hours=hours)
    date_str = beijing_date.strftime('%Y-%m-%d %H:%M:%S')
    return f'{date_str}.{str(timestamp).split(".")[1]}'


def timestamp_to_time(timestamp: float) -> str:
    """
    时间戳转格式化的时间字符串
    :param timestamp: 秒级时间戳
    :return: 格式化的时间字符串
    """
    second = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    millisecond = 0
    if '.' in str(timestamp):
        millisecond = str(timestamp).split('.')[1]
    return f'{second}.{millisecond}'