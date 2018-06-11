from datetime import datetime
from app import db


USER_TYPE = (
        (1, "普通员工"),
        (2, "操作员"),
        (3, "管理员"),
    )


class User(db.Document):
    meta = {
        'collection': 'user'
    }
    # 姓名
    username = db.StringField()
    # 密码
    password = db.StringField()
    # 用户类别
    category = db.IntField(default=1)

    # 工号
    job_number = db.IntField()
    # 性别
    gender = db.StringField()
    # 电话
    telephone = db.StringField()
    # 职位
    title = db.StringField()
    # 部门
    department = db.StringField()
    # # 受雇时间
    hireDate = db.StringField()

    # 是否通过ESD培训
    train_state = db.BooleanField(default=False)

    created_time = db.DateTimeField(default=datetime.now)