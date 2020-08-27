import time


def get_datetime():
     return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
