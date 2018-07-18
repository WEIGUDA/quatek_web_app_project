import datetime
from app import db


class Gate(db.Document):
    name = db.StringField(default='')  # 闸机名
    number = db.StringField(default='')  # 闸机编号
    category = db.StringField(default='')  # 闸机分类
    hand_max = db.IntField(null=True, default=None)  # 手上限值
    hand_min = db.IntField(null=True, default=None)  # 手下限值
    foot_max = db.IntField(null=True, default=None)  # 脚上限值
    foot_min = db.IntField(null=True, default=None)  # 脚下限值
    is_on = db.BooleanField(default=True)  # 闸机开关状态
    is_online = db.BooleanField(default=True)  # 闸机在线状态
    ip = db.StringField(default='')  # IP地址
    port = db.IntField(null=True, default=None)  # 端口
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)


class Card(db.Document):
    card_number = db.StringField(default='', index=True)  # 卡号
    card_category = db.StringField(  # 卡类别
        default='4',
        choices=(('1', 'vip'),
                 ('2', '只测手'),
                 ('3', '只测脚'),
                 ('4', '手脚同测'),)
    )
    name = db.StringField(default='')  # 姓名
    job_number = db.StringField(default='')  # 工号
    department = db.StringField(default='')  # 部门
    gender = db.StringField(default='M', choices=(('M', '男'), ('F', '女')),)  # 性别
    note = db.StringField(default='')  # 其他说明
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)


class CardTest(db.Document):
    test_id = db.StringField(default='')  # 是否检测
    test_result = db.StringField(default='')  # 通行结果
    test_value = db.StringField(default='')  # 手腕检测值
    hand = db.IntField(null=True, default=None)  # 左脚检测值
    left_foot = db.IntField(null=True, default=None)  # 右脚检测值
    right_foot = db.IntField(null=True, default=None)  # 所属用户
    job_number = db.StringField(default='')  # 工号
    gate_number = db.StringField(default='')  # 闸机编号
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
