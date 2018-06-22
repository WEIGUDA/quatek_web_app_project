from datetime import datetime
from app import db


class Attendance(db.Document):
    meta = {
        'collection': 'attendance'
    }

    # 是否出勤
    state = db.StringField()
    # 出勤时间
    working_time = db.StringField()

    # 所属用户
    job_number = db.StringField()

    created_time = db.DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.state = dic.get('state')
        self.working_time = dic.get('working_time')
        self.job_number = dic.get('job_number')


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
    card_id = db.StringField()
    # 卡类别
    category = db.IntField(default=3)
    # 所属用户
    job_number = db.StringField()
    # 所属部门
    department = db.StringField()

    created_time = db.DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.card_id = dic.get('card_id')
        self.category = int(dic.get('category'))
        self.job_number = dic.get('job_number')
        self.department = dic.get('department')


class Machine(db.Document):
    meta = {
        'collection': 'machine'
    }

    # 闸机类型
    machine_type = db.StringField()
    # 闸机名
    machine_name = db.StringField()
    # 闸机编号
    machine_number = db.StringField()
    # 手上限值
    hand_upper = db.IntField()
    # 手下限值
    hand_lower = db.IntField()
    # 脚上限值
    foot_upper = db.IntField()
    # 脚下限值
    foot_lower = db.IntField()
    # 闸机开关状态
    state = db.StringField()

    created_time = db.DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.machine_type = dic.get('machine_type')
        self.machine_name = dic.get('machine_name')
        self.machine_number = dic.get('machine_number')
        self.hand_upper = int(dic.get('hand_upper'))
        self.hand_lower = int(dic.get('hand_lower'))
        self.foot_upper = int(dic.get('foot_upper'))
        self.foot_lower = int(dic.get('foot_lower'))
        self.state = dic.get('state')


class StaticTest(db.Document):
    meta = {
        'collection': 'static_test'
    }

    # 是否检测
    test_state = db.StringField()
    # 通行结果
    test_result = db.StringField()
    # 手腕检测值
    hand = db.IntField()
    # 左脚检测值
    left_foot = db.IntField()
    # 右脚检测值
    right_foot = db.IntField()
    # 所属用户
    job_number = db.StringField()

    created_time = db.DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.test_state = dic.get('test_state')
        self.test_result = dic.get('test_result')
        self.hand = int(dic.get('hand'))
        self.left_foot = int(dic.get('left_foot'))
        self.right_foot = int(dic.get('right_foot'))
        self.job_number = dic.get('job_number')


if __name__ == "__main__":
    pass