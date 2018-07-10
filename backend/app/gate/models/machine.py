from . import *


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













