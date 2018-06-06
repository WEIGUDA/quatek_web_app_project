from . import *
from app.users.models.user import User

main = Blueprint('user', __name__)


@main.route("/")
def hello():
    return "<h3>hello world</h3>"