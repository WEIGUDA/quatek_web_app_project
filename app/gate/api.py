from flask import Blueprint
from flask import request
from flask import jsonify


from flask_restful import Api, Resource


from app.gate.models import Machine
from app.gate.models import Attendance
from app.gate.models import Card
from app.gate.models import StaticTest


gate_blueprint = Blueprint('gate', __name__)
gate_api = Api(gate_blueprint)


def get_machine(machine):
    machine_dic = dict(
        machine_type=machine.machine_type,
        machine_name=machine.machine_name,
        machine_number=machine.machine_number,
        hand_upper=machine.hand_upper,
        hand_lower=machine.hand_lower,
        foot_upper=machine.foot_upper,
        foot_lower=machine.foot_lower,
        state=machine.state,
    )
    return machine_dic


class MachineResource(Resource):
    def get(self):
        args = request.args
        machine_number = args.get('machine_number')
        machine_type = args.get('machine_type')
        setoff = args.get('setoff')
        limit = args.get('limit')

        try:
            if machine_number is not None and machine_type is None and setoff is None and limit is None:
                machine = Machine.objects(machine_number=machine_number).first()
                machine_dic = get_machine(machine)
                return jsonify(machine_dic)
            if machine_number is None and machine_type is None and setoff is None and limit is None:
                machines = Machine.objects.all()
                machine_list = []
                for machine in machines:
                    machine_dic = get_machine(machine)
                    machine_list.append(machine_dic)
                return jsonify(machine_list)
            if machine_number is None and machine_type is not None and setoff is not None and limit is not None:
                machines = Machine.objects(machine_type=machine_type).skip(int(setoff)).limit(int(limit))
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
        hand_upper = json.get('hand_upper', '')
        hand_lower = json.get('hand_lower', '')
        foot_upper = json.get('foot_upper', '')
        foot_lower = json.get('foot_lower', '')
        state = json.get('state', 'false')

        dic = dict(
            machine_type=machine_type,
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
            hand_upper = json.get('hand_upper', machine.hand_upper)
            hand_lower = json.get('hand_lower', machine.hand_lower)
            foot_upper = json.get('foot_upper', machine.foot_upper)
            foot_lower = json.get('foot_lower', machine.foot_lower)
            state = json.get('state', machine.state)

            try:
                machine.update(
                    machine_type=machine_type,
                    machine_name=machine_name,
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


gate_api.add_resource(MachineResource, '/gate/machine')


def get_static(test):
    test_dic = dict(
        test_state=test.test_state,
        test_result=test.test_result,
        hand=test.hand,
        left_foot=test.left_foot,
        right_foot=test.right_foot,
        job_number=test.job_number,
        machine_number=test.machine_number,
    )
    return test_dic


class StaticResource(Resource):
    def get(self):
        args = request.args
        job_number = args.get('job_number')
        setoff = args.get('setoff')
        limit = args.get('limit')

        try:
            tests = []
            if job_number is not None and setoff is None and limit is None:
                tests = StaticTest.objects(job_number=job_number).all()
            if job_number is not None and setoff is not None and limit is not None:
                tests = StaticTest.objects(job_number=job_number).skip(int(setoff)).limit(int(limit))
            test_list = []
            for test in tests:
                test_dic = get_static(test)
                test_list.append(test_dic)
            return jsonify(test_list)
        except:
            message = "get static tests failed"
            return message

    def post(self):
        json = request.json
        test_state = json.get('test_state')
        test_result = json.get('test_result')
        hand = json.get('hand')
        left_foot = json.get('left_foot')
        right_foot = json.get('right_foot')
        job_number = json.get('job_number')
        machine_number = json.get('machine_number')

        dic = dict(
            test_state=test_state,
            test_result=test_result,
            hand=hand,
            left_foot=left_foot,
            right_foot=right_foot,
            job_number=job_number,
            machine_number=machine_number,
        )

        all_exist = True
        for key in dic.keys():
            if dic[key] is None:
                all_exist = False

        try:
            if all_exist:
                static_test = StaticTest()
                static_test.set_attribute(dic)
                static_test.save()
                message = "{}'s static test add successfully".format(job_number)
            else:
                message = "please check if any test record is ignored."
            return message
        except:
            message = "static test add failed"
            return message

    def delete(self):
        args = request.args
        job_number = args.get('job_number')
        try:
            tests = StaticTest.objects(job_number=job_number).all()
            for test in tests:
                test.delete()
            message = "{}'s tests have been deleted successfully".format(job_number)
            return message
        except:
            message = "{}'s tests have been deleted successfully".format(job_number)
            return message


gate_api.add_resource(StaticResource, '/gate/static_test')


def get_card(card):
    card_dic = dict(
        card_id=card.card_id,
        category=card.category,
        job_number=card.job_number,
        department=card.department,
    )
    return card_dic


class CardResource(Resource):
    def get(self):
        args = request.args
        department = args.get('department')
        setoff = args.get('setoff')
        limit = args.get('limit')

        try:
            cards = []
            if department is not None and setoff is None and limit is None:
                cards = Card.objects(department=department).all()
            if department is not None and setoff is not None and limit is not None:
                cards = Card.objects(department=department).skip(int(setoff)).limit(int(limit))
            card_list = []
            for card in cards:
                card_dic = get_card(card)
                card_list.append(card_dic)
            return jsonify(card_list)
        except:
            message = "get cards failed"
            return message

    def post(self):
        json = request.json
        card_id = json.get('card_id', '')
        category = json.get('category')
        job_number = json.get('job_number', '')
        department = json.get('department', '')

        dic = dict(
            card_id=card_id,
            category=category,
            job_number=job_number,
            department=department,
        )
        try:
            message = ''
            if card_id is not None:
                card = Card.objects(card_id=card_id).first()
                if card:
                    message = "Card {} has been added already, please use patch".format(card_id)
                else:
                    card = Card()
                    card.set_attribute(dic)
                    card.save()
                    message = "card {} add successfully".format(card_id)
            else:
                message = "Card id should not be ignored."
            return message
        except:
            message = "card add failed"
            return message

    def patch(self):
        json = request.json
        card_id = json.get('card_id')
        if card_id is not None:
            card = Card.objects(card_id=card_id).first()
            category = json.get('category', card.category)
            job_number = json.get('job_number', card.job_number)
            department = json.get('department', card.department)

            try:
                card.update(
                    category=category,
                    job_number=job_number,
                    department=department,
                )
                message = "card {} update successfully".format(card_id)
                return message
            except:
                message = "card {} update failed".format(card_id)
                return message
        else:
            message = "Card id should not be ignored."
            return message

    def delete(self):
        args = request.args
        card_id = args.get('card_id')
        try:
            card = Card.objects(card_id=card_id).first()
            card.delete()
            message = "card {} delete successfully".format(card_id)
            return message
        except:
            message = "card {} delete failed".format(card_id)
            return message


gate_api.add_resource(CardResource, '/gate/card')


def get_attendance(attendance):
    attendance_dic = dict(
        state=attendance.state,
        working_time=attendance.working_time,
        job_number=attendance.job_number,

    )
    return attendance_dic


class AttendanceResource(Resource):
    def get(self):
        args = request.args
        job_number = args.get('job_number')
        setoff = args.get('setoff')
        limit = args.get('limit')

        try:
            attendances = []
            if job_number is not None and setoff is None and limit is None:
                attendances = Attendance.objects(job_number=job_number).all()
            if job_number is not None and setoff is not None and limit is not None:
                attendances = Attendance.objects(job_number=job_number).skip(int(setoff)).limit(int(limit))
            attendance_list = []
            for attendance in attendances:
                attendance_dic = get_attendance(attendance)
                attendance_list.append(attendance_dic)
            return jsonify(attendance_list)
        except:
            message = "get attendances failed"
            return message

    def post(self):
        json = request.json
        state = json.get('state')
        working_time = json.get('working_time')
        job_number = json.get('job_number')

        dic = dict(
            state=state,
            working_time=working_time,
            job_number=job_number,
        )

        all_exist = True
        for key in dic.keys():
            if dic[key] is None:
                all_exist = False

        try:
            if all_exist:
                attendance = Attendance()
                attendance.set_attribute(dic)
                attendance.save()
                message = "{}'s attendance add successfully".format(job_number)
            else:
                message = "please check if any attendance record is ignored."
            return message
        except:
            message = "attendance add failed"
            return message

    def delete(self):
        args = request.args
        job_number = args.get('job_number')
        try:
            attendances = Attendance.objects(job_number=job_number).all()
            for attendance in attendances:
                attendances.delete()
            message = "{}'s attendances have been deleted successfully".format(job_number)
            return message
        except:
            message = "{}'s attendances have been deleted successfully".format(job_number)
            return message


gate_api.add_resource(AttendanceResource, '/gate/attendance')

