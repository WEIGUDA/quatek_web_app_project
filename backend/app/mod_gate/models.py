import datetime
from app import db


class Gate(db.DynamicDocument):
    name = db.StringField(default='')  # 闸机名
    number = db.StringField(default='')  # 闸机编号
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
    # 进出标志 name1:1|name2:0|name3 0:可进可出, 1:禁止进入/可出, 2:禁止出去/可进, 3:禁止进出  or all:所有闸机都可进可出
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
    card_counter = db.SequenceField(collection_name='card_counter')  # 闸机卡号编号


class CardTest(db.DynamicDocument):
    log_id = db.StringField(default='')  # 记录流水号
    card_counter = db.StringField(default='')  # 卡片编号(内部, 1, 2, 3)
    card_number = db.StringField(default='')  # 卡片号码
    card_category = db.StringField(default='')  # 卡片类型(vip, 手脚都测...)
    in_out_symbol = db.StringField(default='')  # 进出标志: 闸机上是进还是出
    mc_id = db.StringField(default='')  # 闸机 mc id
    test_datetime = db.DateTimeField()  # 测试时间
    test_result = db.StringField(default='')  # 是否通过 1:通过 0:不通过
    is_tested = db.StringField(default='')  # 是否测试 1:测试 0:不测试
    hand = db.StringField(default='')  # 手腕检测值
    left_foot = db.StringField(default='')  # 左脚检测值
    right_foot = db.StringField(default='')  # 右脚检测值
    after_erg = db.StringField(default='')  # ERG后的值
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
