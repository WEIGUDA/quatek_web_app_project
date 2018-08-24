import datetime
from app import db


class SystemConfig(db.DynamicDocument):
    """ 系统设置表
    """
    smtp_host = db.StringField(default='')
    smtp_port = db.IntField(default=None)
    smtp_use_ssl = db.BooleanField(default=True)
    emails = db.StringField(default='')
    work_hours = db.StringField(default='8:00-18:00')
