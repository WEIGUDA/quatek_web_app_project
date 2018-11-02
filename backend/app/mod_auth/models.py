import datetime
from app import db


class User(db.DynamicDocument):
    """ for card user
    """
    username = db.StringField(default='', unique=True)  # 用户名
    password = db.StringField(default='')  # 密码hash
    birthday = db.DateTimeField(default=datetime.date.today)  # 生日
    telephone = db.StringField(default='')  # 电话
    position = db.StringField(default='')  # 职位
    hire_date = db.DateTimeField(default=datetime.date.today)  # 入职时间
    is_trained = db.BooleanField(default=False)  # 是否通过ESD培训
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
    permissions = db.ListField(default=[])  # 权限

    def __str__(self):
        return f'<User> {self.to_json()}'


class Permission(db.DynamicDocument):
    """permission records
    """
    name = db.StringField(default='')
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
