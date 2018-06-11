from flask import Blueprint

from app.users.models import User

user = Blueprint('user', __name__)


@user.route("/")
def hello():
    try:
        user = User.objects(username='chandler').first()
        if user:
            message = "<h3>chandler has been added already.</h3>"
        else:
            user = User(
                username='chandler',
                password='chandler233',
                is_completed=False,
            )
            user.save()
            message = "<h3>add chandler successfully</h3>"
    except:
        message = "<h3>hello world</h3>"
    return message