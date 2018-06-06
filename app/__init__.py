import time

from flask import Flask
from werkzeug.utils import import_string
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 写个函数返回本地时间
def current_time():
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime()
    dt = time.strftime(format, value)
    return dt


# 定义一个能被所有数据模型继承使用的基类
class ModelHelper(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    # 利用请求上下文添加和提交
    def save(self):
        db.session.add(self)
        db.session.commit()

    # 利用请求上下文删除和提交
    def delete(self):
        db.session.delete(self)
        db.session.commit()


blueprints = [
    'app.users.routes:user',

    'app.gate.routes:machine',
    'app.gate.routes:card',
    'app.gate.routes:staticTest',
    'app.gate.routes:attendance',
]


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    for name in blueprints:
        bp = import_string(name)
        app.register_blueprint(bp)

    return app