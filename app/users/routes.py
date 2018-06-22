from flask import Blueprint
from flask import request
from flask import jsonify
from flask_restful import Api, Resource

from app.users.models import User

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route("/")
def hello():
    try:
        user = User.objects(username='chandler').first()
        if user:
            message = "<h3>chandler has been added already.</h3>"
        else:
            user = User(
                username='chandler',
                password='chandler233',
            )
            user.save()
            message = "<h3>add chandler successfully</h3>"
    except:
        message = "<h3>hello world</h3>"
    return message


class UserResource(Resource):
    def get(self):
        args = request.args
        category = args.get('category', '1')
        setoff = int(args.get('setoff', '0'))
        limit = int(args.get('limit', '10'))

        try:
            users = User.objects(category=category).skip(setoff).limit(limit)
            user_list = []
            for user in users:
                user_dic = dict(
                    category=category,
                    username=user.username,
                    password=user.password,
                    job_number=user.job_number,
                    gender=user.gender,
                    telephone=user.telephone,
                    title=user.title,
                    department=user.department,
                    hire_date=user.hire_date,
                    train_state=user.train_state,
                )
                user_list.append(user_dic)
            return jsonify(user_list)
        except:
            message = "get users failed"
            return message

    def post(self):
        json = request.json
        category = json.get('category', '')
        username = json.get('username', '')
        password = json.get('password', '')
        job_number = json.get('job_number')
        gender = json.get('gender', '')
        telephone = json.get('telephone', '')
        title = json.get('title', '')
        department = json.get('department', '')
        hire_date = json.get('hire_date', '')
        train_state = json.get('train_state', 'false')

        dic = dict(
            category=category,
            username=username,
            password=password,
            job_number=job_number,
            gender=gender,
            telephone=telephone,
            title=title,
            department=department,
            hire_date=hire_date,
            train_state=train_state,
        )

        try:
            message = ''
            if job_number is not None:
                user = User.objects(job_number=job_number).first()
                if user:
                    message = "User {} {} has been added already, please use patch".format(username, job_number)
                else:
                    user = User()
                    user.set_attribute(dic)
                    user.save()
                    message = "user {} {} add successfully".format(username, job_number)
            else:
                message = "Job number should not be ignored."
            return message
        except:
            message = "user add failed"
            return message

    def patch(self):
        json = request.json
        job_number = json.get('job_number')
        if job_number is not None:
            user = User.objects(job_number=job_number).first()
            username = json.get('username', user.username)
            password = json.get('password', user.password)
            category = json.get('category', user.category)
            gender = json.get('gender', user.gender)
            telephone = json.get('telephone', user.telephone)
            title = json.get('title', user.title)
            department = json.get('department', user.department)
            hire_date = json.get('hire_date', user.hire_date)
            train_state = json.get('train_state', user.train_state)

            try:
                user.update(
                    username=username,
                    password=password,
                    category=category,
                    gender=gender,
                    telephone=telephone,
                    title=title,
                    department=department,
                    hire_date=hire_date,
                    train_state=train_state,
                )
                message = "user {} job_number {} update successfully".format(username, job_number)
                return message
            except:
                message = "user {} job_number {} update failed".format(username, job_number)
                return message
        else:
            message = "job number should not be ignored."
            return message

    def delete(self):
        args = request.args
        job_number = args.get('job_number')
        try:
            user = User.objects(job_number=job_number).first()
            user.delete()
            message = "job_number {} delete successfully".format(job_number)
            return message
        except:
            message = "job_number {} delete failed".format(job_number)
            return message


user_api = Api(user_blueprint)
user_api.add_resource(UserResource, '/user')


