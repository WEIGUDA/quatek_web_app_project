import datetime
from app import db


class SystemConfig(db.DynamicDocument):
    """ 系统设置表
    """
    smtp_host = db.StringField(default='')
    smtp_port = db.IntField(default=None)
    smtp_username = db.StringField(default='')
    smtp_password = db.StringField(default='')
    smtp_use_ssl = db.BooleanField(default=True)
    smtp_use_tls = db.BooleanField(default=False)
    emails = db.StringField(default='')
    work_hours = db.StringField(default='8:00-18:00')
    db_type = db.StringField(default='')
    db_name = db.StringField(default='')
    db_host = db.StringField(default='')
    db_port = db.IntField(default=None)
    db_username = db.StringField(default='')
    db_password = db.StringField(default='')
    smtp_need_auth = db.BooleanField(default=True)
    timezone = db.StringField(default='+8')
