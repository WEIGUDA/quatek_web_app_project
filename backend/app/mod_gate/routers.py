import datetime
import json
from flask import Blueprint, request, make_response, current_app, abort, jsonify
from mongoengine.queryset.visitor import Q

from app.mod_gate.models import Gate, Card, CardTest
from app.tasks import update_all_cards_to_mc_task, update_a_card_to_all_mc_task, delete_a_card_from_mc_task

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
            return (gates.to_json(), {'Content-Type': 'application/json'})

    elif request.method == 'POST':
        gates_list = request.json
        return_list = []
        try:
            for index, gate in enumerate(gates_list):
                if index == 0 or not gate:
                    continue
                if len(gate) == 1:
                    continue
                g1 = Gate(name=gate[0],
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
                | Q(department__icontains=query_string)\
                | Q(id=query_string)

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
                    card_number=card[0],
                    card_category=card[1],
                    name=card[2],
                    job_number=card[3],
                    department=card[4],
                    gender=card[5],
                    note=card[6].replace('\r', ''),
                )
                if not c1['note']:
                    c1['note'] = 'default note'

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
            card = Card(card_number=data['card_number'],
                        card_category=data['card_category'],
                        name=data['name'],
                        job_number=data['job_number'],
                        department=data['department'],
                        gender=data['gender'], note=data['note'],
                        belong_to_mc=data['belong_to_mc'])
            card.save()

        except:
            current_app.logger.exception('create card failed')
            abort(500)
        else:
            update_a_card_to_all_mc_task.delay(json.loads(card.to_json()))
            return make_response(card.to_json())

    elif request.method == 'PATCH':
        data = request.json
        try:
            card = Card.objects.get(id=data['id'])
            card.card_number = data['card_number']
            card.card_category = data['card_category']
            card.name = data['name']
            card.job_number = data['job_number']
            card.department = data['department']
            card.gender = data['gender']
            card.note = data['note']
            card.belong_to_mc = data['belong_to_mc']
            card.save()

        except:
            current_app.logger.exception('create card failed')
            abort(500)
        else:
            update_a_card_to_all_mc_task.delay(json.loads(card.to_json()))
            return make_response(card.to_json())


@bp.route('/cardtests', methods=['GET', 'POST'])
def cardtests():
    if request.method == 'GET':
        query_string = request.args.get('q', None)
        datetime_from = request.args.get('datetime_from', None)
        datetime_to = request.args.get('datetime_to', None)  # '2018-07-20T07:15:00.000Z'

        if datetime_from:
            datetime_from = datetime.datetime.strptime(
                datetime_from, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)

        if datetime_to:
            datetime_to = datetime.datetime.strptime(
                datetime_to, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)

        q_object = Q(test_datetime__gte=datetime_from) \
            & Q(test_datetime__lte=datetime_to)

        if query_string:
            gates = Gate.objects.filter(name__icontains=query_string)
            gates_mc_ids = []
            if gates:
                for gate in gates:
                    gates_mc_ids.append(gate['mc_id'])

                q_object = (q_object & Q(card_number__icontains=query_string)) \
                    | (q_object & Q(mc_id__in=gates_mc_ids))
            else:
                q_object = q_object & Q(card_number__icontains=query_string)

        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 50)

        try:
            cards = CardTest.objects.filter(q_object).order_by('-created_time').skip(int(offset)).limit(int(limit))
            return make_response(cards.to_json())
        except:
            current_app.logger.exception('get cardtests failed')
            abort(500)

    elif request.method == 'POST':
        pass
