import time
from datetime import datetime
from mongoengine import *
connect("quatek")


def current_time():
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime()
    dt = time.strftime(format, value)
    return dt