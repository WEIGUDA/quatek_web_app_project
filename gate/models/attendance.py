from . import *


class Attendance(db.Model, ModelHelper):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Boolean)                   # 是否出勤
    working_time = db.Column(db.Integer)             # 出勤时间

    created_time = db.Column(db.DateTime)













