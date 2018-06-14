from flask import Flask
from werkzeug.utils import import_string
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


blueprints = [
    'app.users.routes.user:main',

    'app.gate.routes.machine:main',
    'app.gate.routes.card:main',
    'app.gate.routes.staticTest:main',
    'app.gate.routes.attendance:main',
]


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    for name in blueprints:
        bp = import_string(name)
        app.register_blueprint(bp)

    return app
