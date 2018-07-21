import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
from flask_cors import CORS


db = MongoEngine()
socketio = SocketIO()
cors = CORS()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # load default config
    app.config.from_pyfile('config_default.py')

    if config is None:
        # load the instance config, if it exists, when not testing
        # load config from instance/dev.py, if exists override the default config, else keep silent
        # config python file format:
        # DEBUG = True
        # ENV = 'development'
        app.config.from_pyfile('config_dev.py', silent=True)
        # load config from instance/pro.py, if exists override the all the configs below,
        # else keep silent; for security in production environment
        app.config.from_pyfile('config_pro.py', silent=True)
    else:
        # load the test config if passed in
        if type(config) is str:
            app.config.from_pyfile(config)
        elif type(config) is dict:
            app.config.from_mapping(config)

    # init extentions
    db.init_app(app)
    socketio.init_app(app)
    cors.init_app(app)

    # register blueprints
    from app.mod_gate.routers import bp as mod_gate_bp
    from app.mod_auth.routers import bp as mod_auth_bp
    app.register_blueprint(mod_gate_bp)
    app.register_blueprint(mod_auth_bp)

    # @app.route('/', methods=['GET', 'POST'])
    # def default():
    #     current_app.logger.debug(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'))
    #     current_app.logger.debug(str(request.data))
    #     current_app.logger.debug(str(request.args))
    #     return make_response(jsonify(
    #         {'request.data': str(request.data),
    #          'request.json': str(request.json),
    #          'request.args': str(request.args),
    #          'request.method': str(request.method),
    #          'request.form': str(request.form),
    #          'request.files': str(request.files),
    #          'request.cookies': str(request.cookies),
    #          'request.mimetype': str(request.mimetype),
    #          'session': str(session),
    #          }))

    # @socketio.on('message')
    # def handle_message(message):
    #     print('received message: ' + message)

    # @socketio.on('json')
    # def handle_json(json):
    #     print('received json: ' + str(json))

    from app.mod_gate.models import Card, CardTest, Gate
    from app.mod_auth.models import User

    @app.shell_context_processor
    def make_shell_context():
        return {'app': app, 'User': User, 'CardTest': CardTest, 'Gate': Gate, 'Card': Card}

    return app
