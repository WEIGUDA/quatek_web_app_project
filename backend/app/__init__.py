import os
from pprint import pprint
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
from flask_cors import CORS
import flask_excel
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


db = MongoEngine()
socketio = SocketIO()
cors = CORS()
jwt = JWTManager()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_pyfile('config_default.py')

    if config is None:
        app.config.from_pyfile('config_dev.py', silent=True)
        app.config.from_pyfile('config_pro.py', silent=True)
    else:
        # load the test config if passed in
        if isinstance(config, str):
            app.config.from_pyfile(config)
        elif isinstance(config, dict):
            app.config.from_mapping(config)

    # init extentions
    db.init_app(app)
    socketio.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    flask_excel.init_excel(app)

    # register blueprints
    from app.mod_gate.routers import bp as mod_gate_bp
    from app.mod_auth.routers import bp as mod_auth_bp
    from app.mod_task.routers import bp as mod_task_bp
    from app.mod_system_config.routers import bp as mod_system_config_bp
    app.register_blueprint(mod_gate_bp)
    app.register_blueprint(mod_auth_bp)
    app.register_blueprint(mod_task_bp)
    app.register_blueprint(mod_system_config_bp)

    from app.mod_gate.models import Card, CardTest, Gate
    from app.mod_auth.models import User

    @app.shell_context_processor
    def make_shell_context():
        return {'app': app, 'User': User, 'CardTest': CardTest, 'Gate': Gate, 'Card': Card}

    if app.config['DEBUG']:
        pprint(app.config)

    return app
