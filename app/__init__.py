import time

from flask import Flask
from werkzeug.utils import import_string
from flask_mongoengine import MongoEngine

db = MongoEngine()


def current_time():
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime()
    dt = time.strftime(format, value)
    return dt


blueprints = [
    'app.users.routes:user_blueprint',

    'app.gate.routes:machine_blueprint',
    'app.gate.routes:card_blueprint',
    'app.gate.routes:staticTest_blueprint',
    'app.gate.routes:attendance_blueprint',
]


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    for name in blueprints:
        bp = import_string(name)
        app.register_blueprint(bp)

    return app