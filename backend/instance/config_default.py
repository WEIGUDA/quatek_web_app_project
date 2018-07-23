import os

ENV = 'production'
DEBUG = False
SECRET_KEY = os.urandom(24)
MONGODB_SETTINGS = {
    'db': 'quatek_web_app',
    'host': '127.0.0.1',
    'port': 27017,
}
REDIS_URL = 'redis://127.0.0.1'
