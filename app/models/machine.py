from . import *


class Machine(DynamicDocument):
    meta = {
        'collection': 'machine'
    }

    # 闸机类型
    machine_type = StringField()
    # 闸机名
    machine_name = StringField()
    # 闸机编号
    machine_number = StringField()
    # 手上限值
    hand_max = IntField()
    # 手下限值
    hand_min = IntField()
    # 脚上限值
    foot_max = IntField()
    # 脚下限值
    foot_min = IntField()
    # 闸机开关状态
    state = StringField()

    created_time = DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.machine_type = dic.get('machine_type')
        self.machine_name = dic.get('machine_name')
        self.machine_number = dic.get('machine_number')
        self.hand_max = int(dic.get('hand_max'))
        self.hand_min = int(dic.get('hand_min'))
        self.foot_max = int(dic.get('foot_max'))
        self.foot_min = int(dic.get('foot_min'))
        self.state = dic.get('state')