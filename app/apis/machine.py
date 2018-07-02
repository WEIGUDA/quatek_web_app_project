from . import *


main = Blueprint('machine', __name__)
machine_api = Api(main)


def get_machine(machine):
    machine_dic = dict(
        machine_type=machine.machine_type,
        machine_name=machine.machine_name,
        machine_number=machine.machine_number,
        hand_max=machine.hand_max,
        hand_min=machine.hand_min,
        foot_max=machine.foot_max,
        foot_min=machine.foot_min,
        state=machine.state,
        created_time=machine.created_time,
    )
    return machine_dic


class MachineResource(Resource):
    def get(self):
        args = request.args
        machine_number = args.get('machine_number')
        setoff = args.get('setoff')
        limit = args.get('limit')

        try:
            # 获取单个机器
            if machine_number is not None and setoff is None and limit is None:
                machine = Machine.objects(machine_number=machine_number).first()
                machine_dic = get_machine(machine)
                return jsonify(machine_dic)
            # 获取所有机器
            if machine_number is None and setoff is None and limit is None:
                machines = Machine.objects.all()
                machine_list = []
                for machine in machines:
                    machine_dic = get_machine(machine)
                    machine_list.append(machine_dic)
                return jsonify(machine_list)
            # 按 setoff 和 limit 获取 machine
            if machine_number is None and setoff is not None and limit is not None:
                machines = Machine.objects().skip(int(setoff)).limit(int(limit))
                machine_list = []
                for machine in machines:
                    machine_dic = get_machine(machine)
                    machine_list.append(machine_dic)
                return jsonify(machine_list)
        except:
            message = "get machines failed"
            return message

    def post(self):
        json = request.json
        machine_type = json.get('machine_type', '')
        machine_name = json.get('machine_name', '')
        machine_number = json.get('machine_number')
        hand_max = json.get('hand_max', '')
        hand_min = json.get('hand_min', '')
        foot_max = json.get('foot_max', '')
        foot_min = json.get('foot_min', '')
        state = json.get('state', 'false')

        dic = dict(
            machine_type=machine_type,
            machine_name=machine_name,
            machine_number=machine_number,
            hand_max=hand_max,
            hand_min=hand_min,
            foot_max=foot_max,
            foot_min=foot_min,
            state=state,
        )
        try:
            if machine_number is not None:
                machine = Machine.objects(machine_number=machine_number).first()
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
        if machine_number is not None:
            machine = Machine.objects(machine_number=machine_number).first()
            machine_type = json.get('machine_type', machine.machine_type)
            machine_name = json.get('machine_name', machine.machine_name)
            hand_max = json.get('hand_max', machine.hand_max)
            hand_min = json.get('hand_min', machine.hand_min)
            foot_max = json.get('foot_max', machine.foot_max)
            foot_min = json.get('foot_min', machine.foot_min)
            state = json.get('state', machine.state)

            try:
                machine.update(
                    machine_type=machine_type,
                    machine_name=machine_name,
                    hand_max=hand_max,
                    hand_min=hand_min,
                    foot_max=foot_max,
                    foot_min=foot_min,
                    state=state,
                )
                message = "machine {} update successfully".format(machine_number)
                return message
            except:
                message = "machine {} update failed".format(machine_number)
                return message
        else:
            message = "Machine number should not be ignored."
            return message

    def delete(self):
        args = request.args
        machine_number = args.get('machine_number')
        try:
            machine = Machine.objects(machine_number=machine_number).first()
            machine.delete()
            message = "{} delete successfully".format(machine_number)
            return message
        except:
            message = "{} delete failed".format(machine_number)
            return message


machine_api.add_resource(MachineResource, '/gate/machine')


def get_machine_template(machine):
    template_dic = dict(
        machine_type=machine.machine_type,
        machine_name=machine.machine_name,
        machine_number=machine.machine_number,
        hand_max=machine.hand_max,
        hand_min=machine.hand_min,
        foot_max=machine.foot_max,
        foot_min=machine.foot_min,
        state=machine.state,
    )
    return template_dic


class MachineTemplate(Resource):
    def get(self):
        args = request.args
        setoff = args.get('setoff', '0')
        limit = args.get('limit', '10')

        try:
            machines = Machine.objects().skip(int(setoff)).limit(int(limit)).order_by("machine_type")
            machine_list = []
            for machine in machines:
                machine_dic = get_machine_template(machine)
                machine_list.append(machine_dic)
            return jsonify(machine_list)
        except:
            message = "get templates failed"
            return message


machine_api.add_resource(MachineTemplate, '/gate/machine/template')