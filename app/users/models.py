import time
from app import db


# 写个函数返回本地时间
def current_time():
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime()
    dt = time.strftime(format, value)
    return dt


# 定义一个能被所有数据模型继承使用的基类
class ModelHelper(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    # 利用请求上下文添加和提交
    def save(self):
        db.session.add(self)
        db.session.commit()

    # 利用请求上下文删除和提交
    def delete(self):
        db.session.delete(self)
        db.session.commit()


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