from datetime import datetime
from app import db
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
    job_number = db.StringField()
    # 性别
    gender = db.StringField()
    # 电话
    telephone = db.StringField()
    # 职位
    title = db.StringField()
    # 部门
    department = db.StringField()
    # # 受雇时间
    hire_date = db.StringField()

    # 是否通过ESD培训
    train_state = db.StringField()

    created_time = db.DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.username = dic.get('username')
        self.password = get_hash(dic.get('password'))
        self.category = int(dic.get('category'))
        self.job_number = dic.get('job_number')
        self.gender = dic.get('gender')
        self.telephone = dic.get('telephone')
        self.title = dic.get('title')
        self.department = dic.get('department')
        self.hire_date = dic.get('hire_date')
        self.train_state = dic.get('train_state')


if __name__ == "__main__":
    print(get_hash("chandler"))