import time
from app import db
from app import ModelHelper


class Attendance(db.Model, ModelHelper):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Boolean)                   # 是否出勤
    working_time = db.Column(db.Integer)             # 出勤时间

    created_time = db.Column(db.DateTime)


CATEGORY_TYPE = (
        (1, "VIP"),
        (2, "只测手"),
        (3, "只测脚"),
        (3, "手脚同测"),
    )


class Card(db.Model, ModelHelper):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)                # 卡号
    category = db.Column(db.Integer, default=1)                 # 卡类别
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # 所属用户

    created_time = db.Column(db.DateTime)


class Machine(db.Model, ModelHelper):
    __tablename__ = 'machine'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))                 # 闸机名
    number = db.Column(db.Integer)                  # 闸机编号
    hand_upper = db.Column(db.Integer)              # 手上限值
    hand_lower = db.Column(db.Integer)              # 手下限值
    foot_upper = db.Column(db.Integer)              # 脚上限值
    foot_lower = db.Column(db.Integer)              # 脚下限值
    state = db.Column(db.Boolean)                   # 闸机开关状态
    created_time = db.Column(db.DateTime)


class StaticTest(db.Model, ModelHelper):
    __tablename__ = 'staticTest'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Boolean)                  # 是否检测
    result = db.Column(db.Boolean)                 # 通行结果
    hand = db.Column(db.Integer)                   # 手腕检测值
    left_foot = db.Column(db.Integer)              # 左脚检测值
    right_foot = db.Column(db.Integer)             # 右脚检测值

    created_time = db.Column(db.DateTime)