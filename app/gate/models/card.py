from . import *


CATEGORY_TYPE = (
        (1, "VIP"),
        (2, "只测手"),
        (3, "只测脚"),
        (3, "手脚同测"),
    )


class Card(db.Model, ModelHelper):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)                # 卡号
    category = db.Column(db.Integer, default=1)                 # 卡类别
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # 所属用户

    created_time = db.Column(db.DateTime)













