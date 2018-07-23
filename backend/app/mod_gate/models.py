import datetime
from app import db


class Gate(db.DynamicDocument):
    name = db.StringField(default='')  # 闸机名
    number = db.StringField(default='')  # 闸机mc id
    category = db.StringField(default='')  # 闸机分类
    mc_id = db.StringField(default='')  # 闸机 mc id
    hand_max = db.IntField(null=True, default=None)  # 手上限值
    hand_min = db.IntField(null=True, default=None)  # 手下限值
    foot_max = db.IntField(null=True, default=None)  # 脚上限值
    foot_min = db.IntField(null=True, default=None)  # 脚下限值
    is_on = db.BooleanField(default=True)  # 闸机开关状态
    is_online = db.BooleanField(default=True)  # 闸机在线状态
    ip = db.StringField(default='')  # IP地址
    port = db.IntField(null=True, default=None)  # 端口
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)


class Card(db.DynamicDocument):
    card_number = db.StringField(default='')  # 卡号
    card_category = db.StringField(  # 卡类别
        default='0',
        choices=(('0', '手脚都测'),
                 ('1', '只测手'),
                 ('2', '只测脚'),
                 ('3', 'vip'),)
    )
    name = db.StringField(default='')  # 姓名
    job_number = db.StringField(default='')  # 工号
    department = db.StringField(default='')  # 部门
    gender = db.StringField(default='1', choices=(('0', '女'), ('1', '男')),)  # 性别
    note = db.StringField(default='')  # 其他说明
    belong_to_mc = db.StringField(default='all')
    # 闸机中权限 name1:1|name2:0|name3 0:可进可出, 1:禁止进入/可出, 2:禁止出去/可进, 3:禁止进出  or all:所有闸机都可进可出
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
    card_counter = db.SequenceField(collection_name='card_counter')  # 闸机卡号编号


class CardTest(db.DynamicDocument):
    gate_number = db.StringField(default='')  # 闸机编号
    test_result = db.StringField(default='')  # 通行结果
    test_value = db.StringField(default='')  # 检测值
    hand = db.IntField(null=True, default=None)  # 手腕检测值
    left_foot = db.IntField(null=True, default=None)  # 左脚检测值
    right_foot = db.IntField(null=True, default=None)  # 右脚检测值
    job_number = db.StringField(default='')  # 工号
    card_number = db.StringField(default='')  # 卡号
    test_datetime = db.DateTimeField()  # 测试时间
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
