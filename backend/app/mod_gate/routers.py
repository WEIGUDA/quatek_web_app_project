import datetime
from flask import Blueprint, request, jsonify, Response, make_response

from app.mod_gate.models import Gate

bp = Blueprint('mod_gate', __name__, url_prefix='/gates')


def get_gate(gate):
    gate_dic = dict(
        machine_type=gate.machine_type,
        machine_name=gate.machine_name,
        gate_number=gate.gate_number,
        hand_max=gate.hand_max,
        hand_min=gate.hand_min,
        foot_max=gate.foot_max,
        foot_min=gate.foot_min,
        state=gate.state,
        created_time=gate.created_time,
    )
    return gate_dic


@bp.route('', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def gates():
    if request.method == 'GET':
        gate_number = request.args.get('gate_number')
        setoff = request.args.get('setoff')
        limit = request.args.get('limit')

        try:
            # 获取单个机器
            if gate_number is not None and setoff is None and limit is None:
                gate = Gate.objects(gate_number=gate_number).first()
                gate_dic = get_gate(gate)
                return jsonify(gate_dic)
            # 获取所有机器
            if not gate_number and not setoff and not limit:
                gates = Gate.objects.all()
                return make_response(gates.to_json())
            # 按 setoff 和 limit 获取 gate
            if gate_number is None and setoff is not None and limit is not None:
                gates = Gate.objects().skip(int(setoff)).limit(int(limit))
                machine_list = []
                for gate in gates:
                    gate_dic = get_gate(gate)
                    machine_list.append(gate_dic)
                return jsonify(machine_list)
        except:
            message = "get gates failed"
            return message

    elif request.method == 'POST':
        json = request.json
        machine_type = json.get('machine_type', '')
        machine_name = json.get('machine_name', '')
        gate_number = json.get('gate_number')
        hand_max = json.get('hand_max', '')
        hand_min = json.get('hand_min', '')
        foot_max = json.get('foot_max', '')
        foot_min = json.get('foot_min', '')
        state = json.get('state', 'false')

        dic = dict(
            machine_type=machine_type,
            machine_name=machine_name,
            gate_number=gate_number,
            hand_max=hand_max,
            hand_min=hand_min,
            foot_max=foot_max,
            foot_min=foot_min,
            state=state,
        )
        try:
            if gate_number is not None:
                gate = Gate.objects(gate_number=gate_number).first()
                if gate:
                    message = "Gate {} has been added already, please use patch".format(gate_number)
                else:
                    gate = Gate()
                    gate.set_attribute(dic)
                    gate.save()
                    message = "gate {} add successfully".format(gate_number)
            else:
                message = "Gate number should not be ignored."
            return message
        except:
            message = "gate add failed"
            return message

    elif request.method == 'PATCH':
        json = request.json
        gate_number = json.get('gate_number')
        if gate_number is not None:
            gate = Gate.objects(gate_number=gate_number).first()
            machine_type = json.get('machine_type', gate.machine_type)
            machine_name = json.get('machine_name', gate.machine_name)
            hand_max = json.get('hand_max', gate.hand_max)
            hand_min = json.get('hand_min', gate.hand_min)
            foot_max = json.get('foot_max', gate.foot_max)
            foot_min = json.get('foot_min', gate.foot_min)
            state = json.get('state', gate.state)

            try:
                gate.update(
                    machine_type=machine_type,
                    machine_name=machine_name,
                    hand_max=hand_max,
                    hand_min=hand_min,
                    foot_max=foot_max,
                    foot_min=foot_min,
                    state=state,
                )
                message = "gate {} update successfully".format(gate_number)
                return message
            except:
                message = "gate {} update failed".format(gate_number)
                return message
        else:
            message = "Gate number should not be ignored."
            return message

    elif request.method == 'DELETE':
        args = request.args
        gate_number = args.get('gate_number')
        try:
            gate = Gate.objects(gate_number=gate_number).first()
            gate.delete()
            message = "{} delete successfully".format(gate_number)
            return message
        except:
            message = "{} delete failed".format(gate_number)
            return message
