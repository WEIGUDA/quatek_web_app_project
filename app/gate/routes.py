from flask import Blueprint

from app.gate.models import Attendance
from app.gate.models import Card
from app.gate.models import Machine
from app.gate.models import StaticTest

attendance = Blueprint('attendance', __name__)
card = Blueprint('card', __name__)
machine = Blueprint('machine', __name__)
staticTest = Blueprint('staticTest', __name__)