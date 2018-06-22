from flask import Blueprint
from flask import request
from flask import jsonify

from flask_restful import Api, Resource, reqparse


from app.gate.models import Attendance
from app.gate.models import Card
from app.gate.models import Machine
from app.gate.models import StaticTest

attendance_blueprint = Blueprint('attendance', __name__)
card_blueprint = Blueprint('card', __name__)
machine_blueprint = Blueprint('machine', __name__)
staticTest_blueprint = Blueprint('staticTest', __name__)


class MachineResource(Resource):
    def get(self):
        args = request.args
        machine_name = args.get('machine_name', '')
        setoff = args.get('setoff', '')
        limit = args.get('limit', '')
        try:
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
        except:
            message = "get machines failed"
            return message

    def post(self):
        json = request.json
        machine_name = json.get('machine_name', '')
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
        try:
            message = ''
            if machine_number is not None:
                machine = Machine.objects(number=machine_number).first()
                if machine:
                    message = "Machine {} has been added already, please use patch".format(machine_number)
                else:
                    machine = Machine()
                    machine.set_attribute(dic)
                    machine.save()
                    message = "machine {} add successfully".format(machine_number)
            else:
                message = "Machine number should not be ignored."
            return message
        except:
            message = "machine add failed"
            return message

    def patch(self):
        json = request.json
        machine_number = json.get('machine_number')
        machine = Machine.objects(number=machine_number).first()
        machine_name = json.get('machine_name', machine.name)
        hand_upper = json.get('hand_upper', machine.hand_upper)
        hand_lower = json.get('hand_lower', machine.hand_lower)
        foot_upper = json.get('foot_upper', machine.foot_upper)
        foot_lower = json.get('foot_lower', machine.foot_lower)
        state = json.get('state', machine.state)
        try:
            machine.update(
                name=machine_name,
                hand_upper=hand_upper,
                hand_lower=hand_lower,
                foot_upper=foot_upper,
                foot_lower=foot_lower,
                state=state,
            )
            message = "machine {} update successfully".format(machine_number)
            return message
        except:
            message = "machine {} update failed".format(machine_number)
            return message

    def delete(self):
        args = request.args
        machine_number = args.get('machine_number')
        try:
            machine = Machine.objects(number=machine_number).first()
            machine.delete()
            message = "{} delete successfully".format(machine_number)
            return message
        except:
            message = "{} delete failed".format(machine_number)
            return message


machine_api = Api(machine_blueprint)
machine_api.add_resource(MachineResource, '/machine')
