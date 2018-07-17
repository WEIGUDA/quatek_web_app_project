import datetime
import os

from flask import Flask, make_response, Response, request, jsonify, abort, redirect, session
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS


db = MongoEngine()
socketio = SocketIO()
cors = CORS()


def utc_now(convert_to_str=False):
    now = datetime.datetime.now(datetime.timezone.utc)
    if convert_to_str:
        return now.strftime('%Y-%m-%d %H:%M:%S %Z')
    return now


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # load default config
    app.config.from_mapping({'ENV': 'production',
                             'DEBUG': False,
                             'SECRET_KEY': os.urandom(24),
                             'MONGODB_SETTINGS': {
                                 'db': 'quatek_web_app',
                                 'host': '127.0.0.1',
                                 'port': 27017,
                                 #  'username': 'webapp',
                                 #  'password': 'pwd123'
                             }
                             })

    if config is None:
        # load the instance config, if it exists, when not testing
        # load config from instance/dev.py, if exists override the default config, else keep silent
        # config python file format:
        # DEBUG = True
        # ENV = 'development'
        app.config.from_pyfile('dev.py', silent=True)
        # load config from instance/pro.py, if exists override the all the configs below,
        # else keep silent; for security in production environment
        app.config.from_pyfile('pro.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(config)

    db.init_app(app)
    socketio.init_app(app)
    cors.init_app(app)

    from app.mod_gate.routers import bp as mod_gate_bp
    from app.mod_auth.routers import bp as mod_auth_bp
    app.register_blueprint(mod_gate_bp)
    app.register_blueprint(mod_auth_bp)

    @app.route('/', methods=['GET', 'POST'])
    def default():
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'))
        print(str(request.data))
        print(str(request.args))
        return make_response(jsonify(
            {'request.data': str(request.data),
             'request.json': str(request.json),
             'request.args': str(request.args),
             'request.method': str(request.method),
             'request.form': str(request.form),
             'request.files': str(request.files),
             'request.cookies': str(request.cookies),
             'request.mimetype': str(request.mimetype),
             'session': str(session),
             }))

    # @socketio.on('message')
    # def handle_message(message):
    #     print('received message: ' + message)

    # @socketio.on('json')
    # def handle_json(json):
    #     print('received json: ' + str(json))w

    return app
