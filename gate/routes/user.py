from gate.routes import *
from gate.models.user import User

main = Blueprint('user', __name__)


@main.route("/")
def hello():
    return "<h3>hello world</h3>"