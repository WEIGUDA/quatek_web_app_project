from . import *


class Attendance(DynamicDocument):
    meta = {
        'collection': 'attendance'
    }

    # 是否出勤
    state = StringField()
    # 出勤时间
    working_time = StringField()
    # 所属用户
    job_number = StringField()
    # 打卡机器
    machine_number = StringField()

    created_time = DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.state = dic.get('state')
        self.working_time = dic.get('working_time')
        self.job_number = dic.get('job_number')
        self.machine_number = dic.get('machine_number')