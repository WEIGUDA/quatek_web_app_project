import datetime
from flask import Blueprint, request, jsonify, make_response, current_app, abort
from mongoengine.queryset.visitor import Q

from app.mod_gate.models import Gate, Card

bp = Blueprint('mod_gate', __name__)


@bp.route('/gates', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def gates():
    if request.method == 'GET':
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 50)

        try:
            gates = Gate.objects.filter().order_by('-created_time').skip(int(offset)).limit(int(limit))
            return make_response(gates.to_json())
        except:
            current_app.logger.exception('get gates failed')
            abort(500)

    elif request.method == 'POST':
        pass


@bp.route('/cards', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def cards():
    query_string = request.args.get('q', None)
    print(query_string)

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
