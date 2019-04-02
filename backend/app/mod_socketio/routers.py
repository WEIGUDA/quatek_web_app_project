import datetime
import json

from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    make_response,
    request,
    send_file,
)
from flask_socketio import emit, send

from app import socketio

bp = Blueprint("mod_socketio", __name__)


@socketio.on("connect")
def test_connect():
    current_app.logger.info("Client connected")


@socketio.on("disconnect")
def test_disconnect():
    current_app.logger.info("Client disconnected")


@socketio.on("test_event")
def handle_test_message(data):
    current_app.logger.info("backend received message: " + str(data))
