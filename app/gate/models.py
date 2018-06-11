from datetime import datetime
from app import db


class Attendance(db.Document):
    meta = {
        'collection': 'attendence'
    }

    # 是否出勤
    state = db.BooleanField(default=False)
    # 出勤时间
    working_time = db.IntField()

    created_time = db.DateTimeField(default=datetime.now)


CARD_TYPE = (
        (1, "VIP"),
        (2, "只测手"),
        (3, "只测脚"),
        (3, "手脚同测"),
    )


class Card(db.Document):
    meta = {
        'collection': 'card'
    }

    # 卡号
    card_id = db.IntField()
    # 卡类别
    category = db.IntField(default=3)
    # 所属用户
    username = db.StringField()

    created_time = db.DateTimeField(default=datetime.now)


class Machine(db.Document):
    meta = {
        'collection': 'machine'
    }

    # 闸机名
    name = db.StringField()
    # 闸机编号
    number = db.IntField()
    # 手上限值
    hand_upper = db.IntField()
    # 手下限值
    hand_lower = db.IntField()
    # 脚上限值
    foot_upper = db.IntField()
    # 脚下限值
    foot_lower = db.IntField()
    # 闸机开关状态
    db.BooleanField(default=False)

    created_time = db.DateTimeField(default=datetime.now)


class StaticTest(db.Document):
    meta = {
        'collection': 'machine'
    }

    # 是否检测
    db.BooleanField(default=False)
    # 通行结果
    db.BooleanField(default=False)
    # 手腕检测值
    foot_lower = db.IntField()
    # 左脚检测值
    left_foot = db.IntField()
    # 右脚检测值
    right_foot = db.IntField()

    created_time = db.DateTimeField(default=datetime.now)