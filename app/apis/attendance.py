from . import *


main = Blueprint('attendance', __name__)
attendance_api = Api(main)


def get_attendance(attendance):
    attendance_dic = dict(
        state=attendance.state,
        working_time=attendance.working_time,
        job_number=attendance.job_number,
        machine_number=attendance.machine_number,
        created_time=attendance.created_time,

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
            # 获取某一用户的所有考勤
            if job_number is not None and setoff is None and limit is None:
                attendances = Attendance.objects(job_number=job_number).all()
            # 按 setoff 和 limit 获取某一用户的考勤
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
        machine_number = json.get('machine_number')

        dic = dict(
            state=state,
            working_time=working_time,
            job_number=job_number,
            machine_number=machine_number,
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


attendance_api.add_resource(AttendanceResource, '/gate/attendance')


def get_attendance_template(attendance, user, card):
    attendance_dic = dict(
        username=user.username,
        job_number=attendance.job_number,
        machine_number=attendance.machine_number,
        category=card.category,
        department=user.department,
        working_time=attendance.working_time,

    )
    return attendance_dic


class AttendanceTemplate(Resource):
    def get(self):
        args = request.args
        setoff = args.get('setoff', '0')
        limit = args.get('limit', '10')

        try:
            attendances = Attendance.objects().skip(int(setoff)).limit(int(limit)).order_by("job_number")
            attendance_list = []
            for attendance in attendances:
                job_number = attendance.job_number
                user = User.objects(job_number=job_number).first()
                card = User.objects(job_number=job_number).first()
                attendance_dic = get_attendance_template(attendance, user, card)
                attendance_list.append(attendance_dic)
            return jsonify(attendance_list)
        except:
            message = "get attendances failed"
            return message


attendance_api.add_resource(AttendanceTemplate, '/gate/attendance/template')