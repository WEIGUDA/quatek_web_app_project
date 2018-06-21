from flask import Blueprint
from flask import request
from flask import jsonify

from flask_restful import Api, Resource, reqparse


from app.gate.models import Attendance
from app.gate.models import Card
from app.gate.models import Machine
from app.gate.models import StaticTest

attendance = Blueprint('attendance', __name__)
card = Blueprint('card', __name__)
machine = Blueprint('machine', __name__)
staticTest = Blueprint('staticTest', __name__)


class MachineResource(Resource):
    def get(self):
        args = request.args
        machine_name = args.get('machine_name', '')
        setoff = args.get('setoff', '')
        limit = args.get('limit', '')
        machines = Machine.objects(name=machine_name).skip(setoff).limit(limit)
        machine_list = []
        for machine in machines:
            machine_dic = dict(
                machine_name=machine.name,
                machine_number=machine.number,
                hand_upper=machine.hand_upper,
                hand_lower=machine.hand_lower,
                foot_upper=machine.foot_upper,
                foot_lower=machine.foot_lower,
                state=machine.state,
            )
            machine_list.append(machine_dic)
        return jsonify(machine_list)

    def post(self):
        try:
            json = request.json
            machine_name = json.get('machine_name')
            machine_number = json.get('machine_number')
            hand_upper = json.get('hand_upper', '')
            hand_lower = json.get('hand_lower', '')
            foot_upper = json.get('foot_upper', '')
            foot_lower = json.get('foot_lower', '')
            state = json.get('state', 'false')

            dic = dict(
                machine_name=machine_name,
                machine_number=machine_number,
                hand_upper=hand_upper,
                hand_lower=hand_lower,
                foot_upper=foot_upper,
                foot_lower=foot_lower,
                state=state,
            )
            machine = Machine(dic)
            machine.save()
            message = "machine add successfully"
            return message
        except:
            message = "machine add successfully"
            return message

    def patch(self):
        json = request.json
        machine_name = json.get('machine_name')
        machine_number = json.get('machine_number')
        hand_upper = json.get('hand_upper', '')
        hand_lower = json.get('hand_lower', '')
        foot_upper = json.get('foot_upper', '')
        foot_lower = json.get('foot_lower', '')
        state = json.get('state', 'false')

        machine = Machine.objects(machine_number=machine_number).first()
        machine.update(
            machine_name=machine_name,
            machine_number=machine_number,
            hand_upper=hand_upper,
            hand_lower=hand_lower,
            foot_upper=foot_upper,
            foot_lower=foot_lower,
            state=state,
            is_completed=True
        )

    def delete(self):
        args = request.args
        machine_number = args.get('machine_number')
        machine = Machine.objects(machine_number=machine_number).first()
        machine.delete()


machine_api = Api(machine)
machine_api.add_resource(MachineResource, '/machine')
