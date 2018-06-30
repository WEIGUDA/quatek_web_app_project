import time
import os

from flask import Flask
from werkzeug.utils import import_string


blueprints = [
    'app.apis.user:main',
    'app.apis.machine:main',
    'app.apis.card:main',
    'app.apis.static:main',
    'app.apis.attendance:main',
]


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # load default config
    app.config.from_mapping(ENV='development',
                            DEBUG=False,
                            SECRET_KEY=os.urandom(24))

    if test_config is None:
        # load config from instance/dev.py, if exists override the default config, else keep silent
        app.config.from_pyfile('dev.py', silent=True)
        # load config from instance/pro.py, if exists override the all the configs below, else keep silent;
        # for security in production environment
        app.config.from_pyfile('pro.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    for name in blueprints:
        bp = import_string(name)
        app.register_blueprint(bp)

    return app