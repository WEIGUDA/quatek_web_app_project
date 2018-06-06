from flask import render_template
from flask import Blueprint

from app.users.models import User

user = Blueprint('user', __name__)


@user.route("/")
def hello():
    return "<h3>hello world</h3>"