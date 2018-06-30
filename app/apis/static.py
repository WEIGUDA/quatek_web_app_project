from . import *


main = Blueprint('static', __name__)
static_api = Api(main)


def get_static(test, user, card):
    test_dic = dict(
        username=user.username,
        job_number=test.job_number,
        machine_number=test.machine_number,
        category=card.category,
        department=user.department,
        test_result=test.test_result,
        test_state=test.test_state,
        hand=test.hand,
        left_foot=test.left_foot,
        right_foot=test.right_foot,
        created_time=test.created_time,
        test_id=test.test_id,
    )
    return test_dic


class StaticTemplate(Resource):
    def get(self):
        args = request.args
        setoff = args.get('setoff', '0')
        limit = args.get('limit', '10')

        try:
            tests = StaticTest.objects().skip(int(setoff)).limit(int(limit)).order_by("job_number")
            test_list = []
            for test in tests:
                job_number = test.job_number
                user = User.objects(job_number=job_number).first()
                card = Card.objects(job_number=job_number).first()
                test_dic = get_static(test, user, card)
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
            message = "{}'s tests have been deleted failed".format(job_number)
            return message


static_api.add_resource(StaticTemplate, '/gate/static_test')


class SearchStatic(Resource):
    # 姓名 工号 机器号 部门 手腕带 左脚 右脚
    def get(self):
        args = request.args
        content = args.get('query')
        user_kwargs = dict(
            username=content,
            job_number=content,
            department=content,
        )
        test_kwargs = dict(
            machine_number=content,
        )

        user_queries = list(map(lambda i: Q(**{i[0]: i[1]}), user_kwargs.items()))
        test_queries = list(map(lambda i: Q(**{i[0]: i[1]}), test_kwargs.items()))
        user_query = QCombination(QCombination.OR, user_queries)
        test_query = QCombination(QCombination.OR, test_queries)
        users = User.objects(user_query).all()
        tests = StaticTest.objects(test_query).all()

        test_list = []

        for user in users:
            job_number = user.job_number
            tests = StaticTest.objects(job_number=job_number).all()
            for test in tests:
                if test is not None:
                    card = Card.objects(job_number=job_number).first()
                    if card is not None:
                        test_dic = get_static(test, user, card)
                        test_list.append(test_dic)

        for test in tests:
            job_number = test.job_number
            test_id = test.test_id
            user = User.objects(job_number=job_number).first()
            card = Card.objects(job_number=job_number).first()
            if card is not None:
                test_dic = get_static(test, user, card)
                added = False
                for i in test_list:
                    if i["test_id"] == test_id:
                        added = True
                if not added:
                    test_list.append(test_dic)
        return jsonify(test_list)


static_api.add_resource(SearchStatic, '/gate/static_test/search')