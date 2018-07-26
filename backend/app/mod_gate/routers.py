import datetime
import json
from flask import Blueprint, request, make_response, current_app, abort, jsonify
from mongoengine.queryset.visitor import Q

from app.mod_gate.models import Gate, Card, CardTest

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
            return make_response(gates.to_json())

    elif request.method == 'POST':
        gates_list = request.json
        return_list = []
        try:
            for index, gate in enumerate(gates_list):
                if index == 0:
                    continue
                g1 = Gate(name=gate[0],
                          number=gate[1],
                          category=gate[2],
                          mc_id=gate[3],
                          hand_max=gate[4],
                          hand_min=gate[5],
                          foot_max=gate[6],
                          foot_min=gate[7],
                          ip=gate[8],
                          port=gate[9].replace('\r', ''),
                          )
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
                c1 = Card(
                    card_number=card[0],
                    card_category=card[1],
                    name=card[2],
                    job_number=card[3],
                    department=card[4],
                    gender=card[5],
                    note=card[6].replace('\r', ''),
                )
                c1.save()
                return_list.append(c1)
        except:
            current_app.logger.exception('post cards failed')
            abort(500)

        else:
            return make_response(jsonify({'result': len(return_list)}))

    elif request.method == 'DELETE':
        cards_to_delete = json.loads(request.args['delete_array'])
        try:
            for card in cards_to_delete:
                Card.objects.get(pk=card).delete()
        except:
            current_app.logger.exception('delete cards failed')
            abort(500)

        else:
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
            return make_response(card.to_json())


@bp.route('/cardtests', methods=['GET', 'POST'])
def cardtests():
    if request.method == 'GET':
        query_string = request.args.get('q', None)
        datetime_from = request.args.get('datetime_from', None)
        datetime_to = request.args.get('datetime_to', None)  # '2018-07-20T07:15:00.000Z'

        if datetime_from:
            datetime_from = datetime.datetime.strptime(datetime_from, '%Y-%m-%dT%H:%M:%S.%fZ')

        if datetime_to:
            datetime_to = datetime.datetime.strptime(datetime_to, '%Y-%m-%dT%H:%M:%S.%fZ')

        q_object = Q(test_datetime__gte=datetime_from) \
            & Q(test_datetime__lte=datetime_to)

        if query_string:
            q_object = q_object & Q(card_number__icontains=query_string)

            gates = Gate.objects.filter(name__icontains=query_string)
            if gates:
                gates_mc_ids = []
                for gate in gates:
                    gates_mc_ids.append(gate['mc_id'])
                print(gates_mc_ids)

                q_object = (q_object & Q(card_number__icontains=query_string)) \
                    | (q_object & Q(mc_id__in=gates_mc_ids))

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
