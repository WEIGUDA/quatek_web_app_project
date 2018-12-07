try:
    import eventlet
    eventlet.monkey_patch()
except:
    pass

from flask_jwt_extended import JWTManager
import flask_excel
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
from flask import Flask
from pprint import pprint
import os


db = MongoEngine()
socketio = SocketIO()
cors = CORS()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # load default config
    app.config['ENV'] = os.environ.get('ENV', 'production')
    app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'True'.lower()
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
    app.config['MONGODB_DB'] = os.environ.get('MONGODB_DB', 'quatek_web_app')
    app.config['MONGODB_HOST'] = os.environ.get('MONGODB_HOST', '127.0.0.1')
    app.config['MONGODB_PORT'] = os.environ.get('MONGODB_PORT', 27017)
    app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://127.0.0.1')
    app.config['SOCKET_HOST'] = os.environ.get('SOCKET_HOST', '0.0.0.0')
    app.config['SOCKET_PORT'] = os.environ.get('SOCKET_PORT', 5858)
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

    # init extentions
    db.init_app(app)
    socketio.init_app(app, message_queue=app.config['REDIS_URL'])
    cors.init_app(app)
    jwt.init_app(app)
    flask_excel.init_excel(app)

    # register blueprints
    from app.mod_gate.routers import bp as mod_gate_bp
    from app.mod_auth.routers import bp as mod_auth_bp
    from app.mod_task.routers import bp as mod_task_bp
    from app.mod_system_config.routers import bp as mod_system_config_bp
    from app.mod_socketio.routers import bp as mod_socketio_bp
    app.register_blueprint(mod_gate_bp)
    app.register_blueprint(mod_auth_bp)
    app.register_blueprint(mod_task_bp)
    app.register_blueprint(mod_system_config_bp)
    app.register_blueprint(mod_socketio_bp)

    from app.mod_gate.models import Card, CardTest, Gate, CardClassTime
    from app.mod_auth.models import User

    @app.shell_context_processor
    def make_shell_context():
        return {'app': app, 'User': User, 'CardTest': CardTest, 'Gate': Gate, 'Card': Card, 'CardClassTime': CardClassTime}

    if app.config['DEBUG']:
        pprint(app.config)

    return app


__all__ = [db, socketio, jwt, cors, create_app]
