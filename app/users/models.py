import time
from app import db
from app import ModelHelper


USER_CATEGORY = (
        (1, "普通员工"),
        (2, "操作员"),
        (3, "管理员"),
    )


class User(db.Model, ModelHelper):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))          # 姓名
    password = db.Column(db.String(20))          # 密码
    category = db.Column(db.Integer, default=1)  # 用户类别

    job_number = db.Column(db.Integer)           # 工号
    gender = db.Column(db.String(2))             # 性别
    telephone = db.Column(db.String(11))         # 电话
    title = db.Column(db.String(20))             # 职位
    department = db.Column(db.String(20))        # 部门
    hireDate = db.Column(db.String(50))           # 受雇时间

    train_state = db.Column(db.Boolean)          # 是否通过ESD培训

    created_time = db.Column(db.DateTime)