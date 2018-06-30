from . import *


CARD_TYPE = (
        (1, "VIP"),
        (2, "只测手"),
        (3, "只测脚"),
        (3, "手脚同测"),
)


class Card(DynamicDocument):
    meta = {
        'collection': 'card'
    }

    # 卡号
    card_id = StringField()
    # 卡类别
    category = IntField(default=3)
    # 所属用户
    job_number = StringField()

    created_time = DateTimeField(default=datetime.now)

    def set_attribute(self, dic):
        self.card_id = dic.get('card_id')
        self.category = int(dic.get('category'))
        self.job_number = dic.get('job_number')