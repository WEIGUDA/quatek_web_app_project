import datetime
import json
import re

import flask_excel as excel
from flask import (Blueprint, abort, current_app, jsonify, make_response,
                   request, send_file)
from mongoengine.queryset.visitor import Q

import pymongo

from app import mongo
from app.mod_gate.models import Card, CardClassTime, CardTest, Gate
from app.mod_system_config.models import SystemConfig
from app.mod_task.tasks import (delete_a_card_from_mc_task,
                                update_a_card_to_all_mc_task,
                                update_all_cards_to_mc_task)
from app.mod_gate.utils import normalize_card_number

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
            gates = Gate.objects.filter(q_object).order_by(
                '-created_time').skip(int(offset)).limit(int(limit))
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
            cards = Card.objects.filter(q_object).order_by(
                '-created_time').skip(int(offset)).limit(int(limit))

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
                    card_number=normalize_card_number(card[0]),
                    card_category=card[1].strip(),
                    name=card[2].strip(),
                    job_number=card[3].strip(),
                    department=card[4].strip(),
                    gender=card[5].strip(),
                    note=card[6].strip() if card[6] else 'default',
                )

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
            c1 = Card(
                card_number=normalize_card_number(data['card_number']),
                card_category=data['card_category'].strip(),
                name=data['name'].strip(),
                job_number=data['job_number'].strip(),
                department=data['department'].strip(),
                gender=data['gender'].strip(),
                note=data['note'].strip() if data['note'] else 'default',
                belong_to_mc=data['belong_to_mc'].strip(),
                classes=str(data['classes']).strip().split(',') if data['classes'] else ['default']
            )

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
            card.card_number = normalize_card_number(data['card_number'])
            card.card_category = data['card_category'].strip()
            card.name = data['name'].strip()
            card.job_number = data['job_number'].strip()
            card.department = data['department'].strip()
            card.gender = data['gender'].strip()
            card.note = data['note'].strip()
            card.belong_to_mc = data['belong_to_mc'].strip()
            card.classes = str(data['classes']).strip().split(',') if data['classes'] else ['default']
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


@bp.route('/cardtests', methods=['GET', ])
def cardtests():
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
            card_number = normalize_card_number(card_number)

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
                        '测试时间', '测试结果', '是否测试', '手测试值(KΩ)', '左脚测试值(KΩ)', '右脚测试值(KΩ)', 'erg后数值',
                        'rsg', '姓名', '工号'], ]
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
                    in_out_symbol = '出'
                if log['in_out_symbol'] == '1':
                    in_out_symbol = '进'

                # 获得系统时区
                system_config_timezone = int(SystemConfig.objects.get().timezone)
                local_tz = datetime.timezone(datetime.timedelta(hours=system_config_timezone))
                test_datetime = log['test_datetime'].replace(
                    tzinfo=datetime.timezone.utc).astimezone(local_tz).isoformat()

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

                name = ''
                job_number = ''
                try:
                    card = Card.objects.filter(card_number=log['card_number']).first()
                    name = card['name']
                    job_number = card['job_number']

                except:
                    pass

                results.append([log['log_id'], log['card_counter'], log['card_number'], card_category,
                                in_out_symbol, log['mc_id'], test_datetime, test_result, is_tested, log['hand'],
                                log['left_foot'], log['right_foot'], log['after_erg'], log['rsg'], name,
                                job_number])
            return excel.make_response_from_array(results, "xlsx")

        cards = CardTest.objects.filter(q_object).order_by('-test_datetime').skip(int(offset)).limit(int(limit))
        return cards.to_json(), {'Content-Type': 'application/json'}
    except:
        current_app.logger.exception('get cardtests failed')
        abort(500)


@bp.route('/cardtests2', methods=['GET', ])
def cardtests2():
    # get query strings
    datetime_from = request.args.get('datetime_from', None)
    datetime_to = request.args.get('datetime_to', None)  # '2018-07-20T07:15:00.000Z'
    job_number = request.args.get('job_number', None)
    card_number = request.args.get('card_number', None)
    department = request.args.get('department', None)

    query_string_dict = {}

    if datetime_from:
        query_string_dict.setdefault('$and', []).append(
            {'test_datetime': {'$gte': datetime.datetime.strptime(datetime_from, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)}})

    if datetime_to:
        query_string_dict.setdefault('$and', []).append(
            {'test_datetime': {'$lte': datetime.datetime.strptime(datetime_to, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)}})

    if card_number:
        query_string_dict['card_number'] = card_number

    if job_number:
        query_string_dict['job_number'] = job_number

    if department:
        query_string_dict['department'] = department

    # define collections
    log_collection = mongo.db.card_test
    card_collection = mongo.db.card
    system_config_collection = mongo.db.system_config

    # batch query cards
    card_numbers = list(log_collection.find(query_string_dict).distinct('card_number'))
    cards = list(card_collection.find({'card_number': {'$in': card_numbers}}))

    # batch query all in logs related to out logs:
    # 1 找到所以条件下, 为出, 为成功 的 卡号
    query_string_dict_updated_with_out_and_test_succeed = {}
    query_string_dict_updated_with_out_and_test_succeed.update(query_string_dict)
    query_string_dict_updated_with_out_and_test_succeed['in_out_symbol'] = '0'
    query_string_dict_updated_with_out_and_test_succeed['test_result'] = '1'
    out_logs_card_numbers = list(log_collection.find(
        query_string_dict_updated_with_out_and_test_succeed).distinct('card_number'))

    # 1 找到所以条件下, 为进, 为成功, 有出卡号的 logs
    query_string_dict_updated_with_in_and_test_succeed = {}
    query_string_dict_updated_with_in_and_test_succeed.update(query_string_dict)
    query_string_dict_updated_with_in_and_test_succeed['in_out_symbol'] = '1'
    query_string_dict_updated_with_in_and_test_succeed['card_number'] = {'$in': out_logs_card_numbers}
    query_string_dict_updated_with_in_and_test_succeed['test_result'] = '1'
    all_in_logs = list(log_collection.find(query_string_dict_updated_with_in_and_test_succeed).sort('test_datetime'))

    # 获得系统时区
    system_config_timezone = int(system_config_collection.find_one()['timezone'])
    local_tz = datetime.timezone(datetime.timedelta(hours=system_config_timezone))

    try:
        results = [[
            '日期时间(进)', '日期时间(出)', '部门', '工号', '姓名', '机器号(进)', '机器号(出)', '卡类型', '通行结果', '是否检测',
            '手腕带检测(KΩ)', '左脚检测(KΩ)', '右脚检测(KΩ)',
        ], ]
        logs = log_collection.find(query_string_dict)
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
                in_out_symbol = '出'
            if log['in_out_symbol'] == '1':
                in_out_symbol = '进'

            test_datetime = log['test_datetime'].replace(
                tzinfo=datetime.timezone.utc).astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')

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

            # combine card and log
            job_number = ''
            name = ''
            department = ''
            try:
                card = list(filter(lambda card: card['card_number'] == log['card_number'], cards))[0]
                name = card['name']
                job_number = card['job_number']
                department = card['department']
            except:
                pass

            if in_out_symbol == '进':
                results.append([
                    test_datetime, '', department, job_number, name, log['mc_id'], '', card_category, test_result, is_tested,
                    log['hand'], log['left_foot'], log['right_foot'],
                ])

            elif in_out_symbol == '出' and test_result == '通过':

                last_in_log = {}
                try:
                    last_in_log = list(
                        filter(lambda in_log: in_log['card_number'] == log['card_number'] and log['test_datetime'] >= in_log['test_datetime'], all_in_logs))[-1]
                except:
                    pass
                # 如果找到 进 的 log, 则使用进log的 hand, left_foot, right_foot值
                # TODO: 删除该 进 log?
                if last_in_log:
                    results.append([
                        last_in_log[
                            'test_datetime'].replace(
                                tzinfo=datetime.timezone.utc).astimezone(
                                    local_tz).strftime('%Y-%m-%d %H:%M:%S'), test_datetime, department, job_number,
                        name, last_in_log['mc_id'], log['mc_id'], card_category, test_result, is_tested, last_in_log['hand'],
                        last_in_log['left_foot'], last_in_log['right_foot'],
                    ])
            else:
                results.append([
                    '', test_datetime, department, job_number, name, '', log['mc_id'], card_category, test_result, is_tested,
                    log['hand'], log['left_foot'], log['right_foot'],
                ])

        return excel.make_response_from_array(results, "xlsx")

    except:
        current_app.logger.exception('get cardtests failed')
        abort(500)


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
            hand_near_max=gate[8],
            hand_near_min=gate[9],
            foot_near_max=gate[10],
            foot_near_min=gate[11],
        )
        if not g1.hand_max:
            g1.hand_max = 35000
        if not g1.hand_min:
            g1.hand_min = 750
        if not g1.foot_max:
            g1.foot_max = 200000
        if not g1.foot_min:
            g1.foot_min = 200

        if not g1.hand_near_max:
            g1.hand_near_max = 35000
        if not g1.hand_near_min:
            g1.hand_near_min = 750
        if not g1.foot_near_max:
            g1.foot_near_max = 200000
        if not g1.foot_near_min:
            g1.foot_near_min = 200

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
    card_collection = Card._get_collection()
    cards_list = request.get_array(field_name='excel_file')
    return_list = []
    failed_list = []

    for index, card in enumerate(cards_list):
        # 忽略第一行
        if index == 0:
            continue

        card_number = normalize_card_number(card[0])
        card_category = str(card[1]).strip()
        name = str(card[2]).strip()
        job_number = str(card[3]).strip()
        department = str(card[4]).strip()
        gender = str(card[5]).strip()
        note = str(card[6]).strip() if card[6] else 'default'
        classes = str(card[7]).strip().split(',') if card[7] else 'default'
        hid_card_number = ''
        try:
            hid_card_number = str(card[8]).strip()
        except:
            pass

        card_tmp = list(card_collection.find({'job_number': job_number}).limit(1))
        # 如果数据库中找到工号相同的卡, 则覆盖原来的信息
        if card_tmp:
            card_existed = Card(**card_tmp[0])
            card_existed.card_number = card_number
            card_existed.card_category = card_category
            card_existed.name = name
            card_existed.department = department
            card_existed.gender = gender
            card_existed.note = note
            card_existed.classes = classes
            card_existed.hid_card_number = hid_card_number
            try:
                card_existed.save()
                return_list.append(card_existed.to_json())
            except Exception as e:
                failed_list.append((card_existed.to_json(), str(e)))

        else:
            new_card = Card(
                job_number=job_number,
                card_number=card_number,
                card_category=card_category,
                name=name,
                department=department,
                gender=gender,
                note=note,
                classes=classes,
                hid_card_number=hid_card_number,
            )
            try:
                new_card.save()
                return_list.append(new_card.to_json())
            except Exception as e:
                failed_list.append((new_card.to_json(), str(e)))

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
