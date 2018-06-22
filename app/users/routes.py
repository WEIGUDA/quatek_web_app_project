from flask import Blueprint
from flask_restful import Api, Resource

from app.users.models import User

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route("/")
def hello():
    try:
        user = User.objects(username='chandler').first()
        if user:
            message = "<h3>chandler has been added already.</h3>"
        else:
            user = User(
                username='chandler',
                password='chandler233',
            )
            user.save()
            message = "<h3>add chandler successfully</h3>"
    except:
        message = "<h3>hello world</h3>"
    return message


