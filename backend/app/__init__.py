import eventlet
eventlet.monkey_patch()

import os
import json
from pprint import pprint
import click
import flask_excel
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from flask_socketio import SocketIO


db = MongoEngine()
socketio = SocketIO()
cors = CORS()
jwt = JWTManager()
mongo = PyMongo()


def create_app():
    app = Flask(__name__)

    # load default config
    app.config['ENV'] = os.environ.get('ENV', 'production')
    app.config['DEBUG'] = os.environ.get(
        'DEBUG', 'False').lower() == 'True'.lower()
    app.config['TESTING'] = os.environ.get(
        'TESTING', 'False').lower() == 'True'.lower()
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
    app.config['MONGODB_DB'] = os.environ.get('MONGODB_DB', 'quatek_web_app')
    app.config['MONGODB_HOST'] = os.environ.get('MONGODB_HOST', '127.0.0.1')
    app.config['MONGODB_PORT'] = int(os.environ.get('MONGODB_PORT', '27017'))
    app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://127.0.0.1')
    app.config['SOCKET_HOST'] = os.environ.get('SOCKET_HOST', '0.0.0.0')
    app.config['SOCKET_PORT'] = int(os.environ.get('SOCKET_PORT', '5858'))
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    app.config["MONGO_URI"] = "mongodb://{}:{}/{}".format(
        app.config['MONGODB_HOST'],
        app.config['MONGODB_PORT'],
        app.config['MONGODB_DB'])

    # init extentions
    db.init_app(app)
    socketio.init_app(app, message_queue=app.config['REDIS_URL'])
    cors.init_app(app)
    jwt.init_app(app)
    flask_excel.init_excel(app)
    mongo.init_app(app)

    #
    @app.route('/')
    def index():
        return jsonify({'version': '2018.02.02.1'})

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
    from app.mod_system_config.models import SystemConfig
    from app.mod_auth.models import User

    @app.shell_context_processor
    def make_shell_context():
        return {
            'app': app,
            'User': User,
            'CardTest': CardTest,
            'Gate': Gate,
            'Card': Card,
            'CardClassTime': CardClassTime,
            'SystemConfig': SystemConfig,
            'user_collection': mongo.db.user,
            'card_collection': mongo.db.card,
            'card_class_time_collection': mongo.db.card_class_time,
            'gate_collection': mongo.db.gate,
            'system_config_collection': mongo.db.system_config,
            'schedules_collection': mongo.db.schedules, }

    # middleware 初始化 user 数据表
    @app.before_first_request
    def init_app():
        user_collection = mongo.db.user
        if user_collection.count_documents({}) == 0:
            user_collection.insert_one(
                {'username': 'quatek', 'password': 'quatek'})
            app.logger.info('created a default user for user collection')

    if app.config['DEBUG']:
        pprint({k: v for k, v in app.config.items() if k in [
               'DEBUG', 'ENV', 'TESTING', 'MONGO_URI', 'REDIS_URL',
               'SOCKET_HOST', 'SOCKET_PORT']})

    return app
