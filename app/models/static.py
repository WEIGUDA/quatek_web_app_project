from . import *
from uuid import uuid1


class StaticTest(DynamicDocument):
    meta = {
        'collection': 'static_test'
    }

    test_id = StringField()
    # 是否检测
    test_state = StringField()
    # 通行结果
    test_result = StringField()
    # 手腕检测值
    hand = IntField()
    # 左脚检测值
    left_foot = IntField()
    # 右脚检测值
    right_foot = IntField()
    # 所属用户
    job_number = StringField()
    # 所属闸机
    machine_number = StringField()

    created_time = DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.test_id = str(uuid1())
        self.test_state = dic.get('test_state')
        self.test_result = dic.get('test_result')
        self.hand = int(dic.get('hand'))
        self.left_foot = int(dic.get('left_foot'))
        self.right_foot = int(dic.get('right_foot'))
        self.job_number = dic.get('job_number')
        self.machine_number = dic.get('machine_number')


if __name__ == "__main__":
    pass