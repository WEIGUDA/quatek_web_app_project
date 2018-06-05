from flask import Flask
from werkzeug.utils import import_string

from models import db


blueprints = [
    'gate.routes.user:main',
    'gate.routes.machine:main',
    'gate.routes.card:main',
    'gate.routes.test:main',
    'gate.routes.attendance:main',
]


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    for name in blueprints:
        bp = import_string(name)
        app.register_blueprint(bp)

    return app