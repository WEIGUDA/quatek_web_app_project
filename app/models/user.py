from . import *
from hashlib import sha256


USER_TYPE = (
        (1, "普通员工"),
        (2, "操作员"),
        (3, "管理员"),
    )


def get_hash(str):
    str = bytes(str, encoding='utf-8')
    hash = sha256()
    hash.update(str)
    return hash.hexdigest()


class User(DynamicDocument):
    meta = {
        'collection': 'user'
    }
    # 姓名
    username = StringField()
    # 密码
    password = StringField()
    # 用户类别
    category = IntField(default=1)

    # 工号
    job_number = StringField()
    # 性别
    gender = StringField()
    # 出生
    birthday = StringField()
    # 电话
    telephone = StringField()
    # 职位
    title = StringField()
    # 部门
    department = StringField()
    # # 受雇时间
    hire_date = StringField()

    # 是否通过ESD培训
    train_state = StringField()

    created_time = DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.username = dic.get('username')
        self.password = get_hash(dic.get('password'))
        self.category = int(dic.get('category'))
        self.job_number = dic.get('job_number')
        self.gender = dic.get('gender')
        self.birthday = dic.get('birthday')
        self.telephone = dic.get('telephone')
        self.title = dic.get('title')
        self.department = dic.get('department')
        self.hire_date = dic.get('hire_date')
        self.train_state = dic.get('train_state')