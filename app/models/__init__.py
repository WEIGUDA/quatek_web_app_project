import time
from datetime import datetime
from mongoengine import *

from instance.dev import MONGODB_DB
connect(MONGODB_DB)


def current_time():
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime()
    dt = time.strftime(format, value)
    return dt