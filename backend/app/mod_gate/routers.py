import datetime
import json
from flask import Blueprint, request, make_response, current_app, abort, jsonify, send_file
from mongoengine.queryset.visitor import Q
import flask_excel as excel


from app.mod_gate.models import Gate, Card, CardTest, CardClassTime
from app.mod_task.tasks import update_all_cards_to_mc_task, update_a_card_to_all_mc_task, delete_a_card_from_mc_task

bp = Blueprint('mod_gate', __name__)


@bp.route('/gates', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def gates():
    if request.method == 'GET':
        query_string = request.args.get('q', None)
        q_object = Q()

        if query_string:
            q_object = q_object | Q(category__icontains=query_string)

        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 50)

        try:
            gates = Gate.objects.filter(q_object).order_by('-created_time').skip(int(offset)).limit(int(limit))
        except:
            current_app.logger.exception('get gates failed')
            abort(500)
        else:
            return gates.to_json(), {'Content-Type': 'application/json'}

    elif request.method == 'POST':
        gates_list = request.json
        return_list = []
        try:
            for index, gate in enumerate(gates_list):
                if index == 0 or not gate:
                    continue
                if len(gate) == 1:
                    continue
                g1 = Gate(
                    name=gate[0],
                    number=gate[1],
                    category=gate[2],
                    mc_id=gate[3],
                    hand_max=gate[4],
                    hand_min=gate[5],
                    foot_max=gate[6],
                    foot_min=gate[7],
                )
                if not g1.hand_max:
                    g1.hand_max = 35000
                if not g1.hand_min:
                    g1.hand_min = 750
                if not g1.foot_max:
                    g1.foot_max = 200000
                if not g1.foot_min:
                    g1.foot_min = 200
                g1.save()
                return_list.append(g1)
        except:
            current_app.logger.exception('post gates failed')
            abort(500)
        else:
            return make_response(jsonify({'result': len(return_list)}))


@bp.route('/cards', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def cards():
    if request.method == 'GET':
        query_string = request.args.get('q', None)

        q_object = Q()

        if query_string:
            q_object = q_object \
                | Q(card_number__icontains=query_string)\
                | Q(card_category__icontains=query_string)\
                | Q(name__icontains=query_string)\
                | Q(job_number__icontains=query_string)\
                | Q(department__icontains=query_string)

        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 50)

        try:
            cards = Card.objects.filter(q_object).order_by('-created_time').skip(int(offset)).limit(int(limit))

        except:
            current_app.logger.exception('get cards failed')
            abort(500)
        else:
            return make_response(cards.to_json())

    elif request.method == 'POST':
        cards_list = request.json
        return_list = []
        try:
            for index, card in enumerate(cards_list):
                if index == 0:
                    continue
                if len(card) == 1:
                    continue

                c1 = Card(
                    card_number=card[0].upper().rjust(8, '0').strip(),
                    card_category=card[1].strip(),
                    name=card[2].strip(),
                    job_number=card[3].strip(),
                    department=card[4].strip(),
                    gender=card[5].strip(),
                    note=card[6].strip(),
                )

                if len(c1.card_number) > 8:
                    c1.card_number = hex(int(c1.card_number))[2:].upper().rjust(8, '0')

                if not c1.note:
                    c1.note = 'default'

                c1.save()

                return_list.append(c1)
        except:
            current_app.logger.exception('post cards failed')
            abort(500)

        else:
            update_all_cards_to_mc_task.delay()
            return make_response(jsonify({'result': len(return_list)}))

    elif request.method == 'DELETE':
        cards_to_delete = json.loads(request.args['delete_array'])
        cards_to_delete2 = []
        try:
            for card in cards_to_delete:
                card_obj = Card.objects.get(pk=card)
                card_2 = json.loads(card_obj.to_json())
                cards_to_delete2.append(card_2)
                card_obj.delete()

        except:
            current_app.logger.exception('delete cards failed')
            abort(500)

        else:
            for card_2 in cards_to_delete2:
                delete_a_card_from_mc_task.delay(card_2)
            return make_response(jsonify({'result': len(cards_to_delete)}))


@bp.route('/cards/create', methods=['POST', 'PATCH'])
def card_create():
    if request.method == 'POST':
        data = request.json
        try:
            c1 = Card(card_number=data['card_number'].upper().rjust(8, '0').strip(),
                      card_category=data['card_category'].strip(),
                      name=data['name'].strip(),
                      job_number=data['job_number'].strip(),
                      department=data['department'].strip(),
                      gender=data['gender'].strip(),
                      note=data['note'].strip(),
                      belong_to_mc=data['belong_to_mc'].strip(),
                      class_time=data['class_time'].strip())

            if len(c1.card_number) > 8:
                c1.card_number = hex(int(c1.card_number))[2:].upper().rjust(8, '0')

            if not c1.note:
                c1.note = 'default'

            c1.save()

        except:
            current_app.logger.exception('create card failed')
            abort(500)
        else:
            update_a_card_to_all_mc_task.delay(json.loads(c1.to_json()))
            return make_response(c1.to_json())

    elif request.method == 'PATCH':
        data = request.json
        try:
            card = Card.objects.get(id=data['id'])
            card.card_number = data['card_number'].upper().rjust(8, '0').strip()
            card.card_category = data['card_category'].strip()
            card.name = data['name'].strip()
            card.job_number = data['job_number'].strip()
            card.department = data['department'].strip()
            card.gender = data['gender'].strip()
            card.note = data['note'].strip()
            card.belong_to_mc = data['belong_to_mc'].strip()
            card.class_time = data['class_time'].strip()
            card.save()

        except:
            current_app.logger.exception('create card failed')
            abort(500)
        else:
            update_a_card_to_all_mc_task.delay(json.loads(card.to_json()))
            return make_response(card.to_json())


@bp.route('/download-cards', methods=['GET', ])
def download_cards():
    cards = [['*card_number', '*card_category(0:vip|1:hands_only|2:feet_only|3:test_both)',
              '*name', '*job_number', '*department', '*gender(0:female|1:male)', 'note', '班别'], ]
    for card in Card.objects.all():
        cards.append([card.card_number, card.card_category, card.name, card.job_number,
                      card.department, card.gender, card.note, card.class_time])
    return excel.make_response_from_array(cards, 'xlsx')


@bp.route('/cardtests', methods=['GET', 'POST'])
def cardtests():
    if request.method == 'GET':
        q_object = Q()

        query_string = request.args.get('q', None)
        datetime_from = request.args.get('datetime_from', None)
        datetime_to = request.args.get('datetime_to', None)  # '2018-07-20T07:15:00.000Z'
        job_number = request.args.get('job_number', None)
        card_number = request.args.get('card_number', None)
        department = request.args.get('department', None)
        is_downloading_excel = request.args.get('is_downloading_excel', None)

        if datetime_from:
            datetime_from = datetime.datetime.strptime(
                datetime_from, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)
            q_object = q_object & Q(test_datetime__gte=datetime_from)

        if datetime_to:
            datetime_to = datetime.datetime.strptime(
                datetime_to, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)
            q_object = q_object & Q(test_datetime__lte=datetime_to)

        if query_string:
            gates = Gate.objects.filter(name__icontains=query_string)
            gates_mc_ids = []
            if gates:
                for gate in gates:
                    gates_mc_ids.append(gate['mc_id'])

            q_object = (q_object & Q(card_number__icontains=query_string)) \
                | (q_object & Q(mc_id__in=gates_mc_ids))

        if card_number:
            if len(card_number) > 8:
                card_number = hex(int(card_number))[2:].upper().rjust(8, '0')

            q_object = q_object & Q(card_number__icontains=card_number)

        if job_number:
            cards = Card.objects.filter(job_number__icontains=job_number)
            q_object = q_object & Q(card_number__in=[card.card_number for card in cards])

        if department:
            cards = Card.objects.filter(department__icontains=department)
            q_object = q_object & Q(card_number__in=[card.card_number for card in cards])

        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 50)

        try:
            if is_downloading_excel:
                results = [['log_id', '卡片编号', '卡片号码', '卡片分类', '进出标志', 'mc id',
                            '测试时间', '测试结果', '是否测试', '手测试值(KΩ)', '左脚测试值(KΩ)', '右脚测试值(KΩ)', 'erg后数值', 'rsg', ], ]
                logs = CardTest.objects.filter(q_object).order_by('-test_datetime').skip(0).limit(100000)
                for log in logs:
                    card_category = ''
                    if log['card_category'] == '0':
                        card_category = 'VIP'
                    if log['card_category'] == '1':
                        card_category = '只测手'
                    if log['card_category'] == '2':
                        card_category = '只测脚'
                    if log['card_category'] == '3':
                        card_category = '手脚都测'

                    in_out_symbol = ''
                    if log['in_out_symbol'] == '0':
                        card_category = '出'
                    if log['in_out_symbol'] == '1':
                        card_category = '进'

                    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                    test_datetime = log['test_datetime'].replace(tzinfo=local_tz).isoformat()

                    test_result = ''
                    if log['test_result'] == '0':
                        test_result = '不通过'
                    if log['test_result'] == '1':
                        test_result = '通过'

                    is_tested = ''
                    if log['is_tested'] == '0':
                        is_tested = '不测试'
                    if log['is_tested'] == '1':
                        is_tested = '测试'

                    results.append([log['log_id'], log['card_counter'], log['card_number'], card_category, in_out_symbol, log['mc_id'],
                                    test_datetime, test_result, is_tested, log['hand'], log['left_foot'], log['right_foot'], log['after_erg'], log['rsg'], ])
                return excel.make_response_from_array(results, "xlsx")

            cards = CardTest.objects.filter(q_object).order_by('-test_datetime').skip(int(offset)).limit(int(limit))
            return cards.to_json(), {'Content-Type': 'application/json'}
        except:
            current_app.logger.exception('get cardtests failed')
            abort(500)

    elif request.method == 'POST':
        pass


@bp.route('/get-card-by-id', methods=['GET', ])
def get_card_by_id():
    query_string = request.args.get('q', None)

    try:
        cards = Card.objects.filter(pk=query_string)

    except:
        current_app.logger.exception('get cards failed')
        abort(500)
    else:
        return make_response(cards.to_json())


@bp.route('/download_gates_upload_template', methods=['GET', ])
def download_gates_upload_template2():
    return send_file('mod_gate/static/闸机上传模版.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@bp.route('/upload_gates_excel', methods=['POST', ])
def upload_gates_excel():
    gates_list = request.get_array(field_name='excel_file')
    return_list = []
    failed_list = []
    for index, gate in enumerate(gates_list):
        if index == 0:
            continue
        g1 = Gate(
            name=gate[0],
            number=str(gate[1]),
            category=gate[2],
            mc_id=str(gate[3]),
            hand_max=gate[4],
            hand_min=gate[5],
            foot_max=gate[6],
            foot_min=gate[7],
        )
        if not g1.hand_max:
            g1.hand_max = 35000
        if not g1.hand_min:
            g1.hand_min = 750
        if not g1.foot_max:
            g1.foot_max = 200000
        if not g1.foot_min:
            g1.foot_min = 200

        try:
            g1.save()
        except Exception as e:
            failed_list.append((g1.to_json(), str(e)))
        else:
            return_list.append(g1.to_json())

    return (jsonify({'result': len(return_list), 'failed': failed_list, 'failed_numbers': len(failed_list)}),
            {'Content-Type': 'application/json'})


@bp.route('/download_cards_upload_template', methods=['GET', ])
def download_cards_upload_template():
    return send_file('mod_gate/static/卡片上传模版.xlsx',
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@bp.route('/upload_cards_excel', methods=['POST', ])
def upload_cards_excel():
    cards_list = request.get_array(field_name='excel_file')
    return_list = []
    failed_list = []

    for index, card in enumerate(cards_list):
        if index == 0:
            continue

        card = Card.objects.filter(card_number=str(card[0]).upper().rjust(
            8, '0').strip(), job_number=str(card[3]).strip()).first()
        if card:
            card.card_category = str(card[1]).strip(),
            card.name = str(card[2]).strip(),
            card.department = str(card[4]).strip(),
            card.gender = str(card[5]).strip(),
            card.note = str(card[6]).strip(),
            card.class_time = str(card[7]).strip()
            card.save()
            continue

        c1 = Card(
            card_number=str(card[0]).upper().rjust(8, '0').strip(),
            card_category=str(card[1]).strip(),
            name=str(card[2]).strip(),
            job_number=str(card[3]).strip(),
            department=str(card[4]).strip(),
            gender=str(card[5]).strip(),
            note=str(card[6]).strip(),
            class_time=str(card[7]).strip()
        )

        if len(c1.card_number) > 8:
            c1.card_number = hex(int(c1.card_number))[2:].upper().rjust(8, '0')

        if not c1.note:
            c1.note = 'default'

        if not c1.class_time:
            c1.class_time = 'default'

        try:
            c1.save()
        except Exception as e:
            failed_list.append((c1.to_json(), str(e)))
        else:
            return_list.append(c1.to_json())

    return jsonify({'result': len(return_list), 'failed': failed_list, 'failed_numbers': len(failed_list)}), {'Content-Type': 'application/json'}


@bp.route('/get-class-times', methods=['GET', ])
def get_class_times():
    class_times = CardClassTime.objects.filter()
    return class_times.to_json(), {'Content-Type': 'application/json'}


@bp.route('/add-class-time', methods=['POST', ])
def add_class_time():
    data = request.json
    class_time = CardClassTime(
        name=data['class_time_name'],
        working_time_from=data['class_time_from'],
        working_time_to=data['class_time_to'])
    class_time.save()
    return jsonify({'result': 'created', 'content': class_time.to_json()}), 201


@bp.route('/delete-class-time', methods=['POST', ])
def delete_class_time():
    data = request.json
    c = CardClassTime.objects.get(id=data['class_time_id'])
    c.delete()
    return jsonify({'result': 'created', 'content': c.to_json()}), 200
