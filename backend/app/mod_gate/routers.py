import datetime
from flask import Blueprint, request, make_response, current_app, abort
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
            return make_response(gates.to_json())
        except:
            current_app.logger.exception('get gates failed')
            abort(500)

    elif request.method == 'POST':
        pass


@bp.route('/cards', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def cards():
    query_string = request.args.get('q', None)

    q_object = Q()

    if query_string:
        q_object = q_object \
            | Q(card_number__icontains=query_string) \
            | Q(card_category__icontains=query_string) \
            | Q(name__icontains=query_string) \
            | Q(job_number__icontains=query_string) \
            | Q(department__icontains=query_string)

    if request.method == 'GET':
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 50)

        try:
            cards = Card.objects.filter(q_object).order_by('-created_time').skip(int(offset)).limit(int(limit))
            return make_response(cards.to_json())
        except:
            current_app.logger.exception('get cards failed')
            abort(500)

    elif request.method == 'POST':
        pass


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
            q_object = (q_object & Q(job_number__icontains=query_string)) | (
                q_object & Q(gate_number__icontains=query_string))

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
