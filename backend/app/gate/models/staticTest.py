from . import *


class StaticTest(db.Model, ModelHelper):
    __tablename__ = 'staticTest'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Boolean)                  # 是否检测
    result = db.Column(db.Boolean)                 # 通行结果
    hand = db.Column(db.Integer)                   # 手腕检测值
    left_foot = db.Column(db.Integer)              # 左脚检测值
    right_foot = db.Column(db.Integer)             # 右脚检测值

    created_time = db.Column(db.DateTime)













