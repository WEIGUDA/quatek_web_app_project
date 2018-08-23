import datetime
from app import db


class User(db.DynamicDocument):
    """ for card user
    """
    username = db.StringField(default='')  # 用户名
    password = db.StringField(default='')  # 密码hash
    birthday = db.DateTimeField(default=datetime.date.today)  # 生日
    telephone = db.StringField(default='')  # 电话
    position = db.StringField(default='')  # 职位
    hire_date = db.DateTimeField(default=datetime.date.today)  # 入职时间
    is_trained = db.BooleanField(default=False)  # 是否通过ESD培训
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)


class Admin(db.DynamicDocument):
    """ for user login
    """
    username = db.StringField(default='')  # 用户名
    password = db.StringField(default='')  # 密码hash
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
