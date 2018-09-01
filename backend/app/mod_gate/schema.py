from datetime import datetime
from sqlalchemy import Column, String, DateTime, Unicode
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Unicode(200), primary_key=True, default='')
    log_id = Column(Unicode(200), default='')  # 记录流水号
    card_counter = Column(Unicode(200), default='')  # 卡片编号(内部, 1, 2, 3)
    card_number = Column(Unicode(200), default='')  # 卡片号码
    card_category = Column(Unicode(200), default='')  # 卡片类型(vip, 手脚都测...)
    in_out_symbol = Column(Unicode(200), default='')  # 进出标志: 闸机上是进还是出
    mc_id = Column(Unicode(200), default='')  # 闸机 mc id
    test_datetime = Column(DateTime(), default=datetime.utcnow)  # 测试时间
    test_result = Column(Unicode(200), default='')  # 是否通过 1:通过 0:不通过
    is_tested = Column(Unicode(200), default='')  # 是否测试 1:测试 0:不测试
    hand = Column(Unicode(200), default='')  # 手腕检测值
    left_foot = Column(Unicode(200), default='')  # 左脚检测值
    right_foot = Column(Unicode(200), default='')  # 右脚检测值
    after_erg = Column(Unicode(200), default='')  # ERG后的值
    rsg = Column(Unicode(200), default='')  # RSG值

    name = Column(Unicode(200), default='')  # 姓名
    job_number = Column(Unicode(200), default='')  # 工号
    department = Column(Unicode(200), default='')  # 部门
    gender = Column(Unicode(200), default='')  # 性别
    note = Column(Unicode(200), default='')  # 其他说明
    # 进出标志 name1:1|name2:0|name3 0:可进可出, 1:禁止进入/可出, 2:禁止出去/可进, 3:禁止进出  or all:所有闸机都可进可出
    belong_to_mc = Column(Unicode(200), default='')
