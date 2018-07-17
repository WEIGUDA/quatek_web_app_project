import datetime
from flask import Blueprint, request, jsonify, make_response, current_app, abort

from app.mod_gate.models import Gate

bp = Blueprint('mod_gate', __name__, url_prefix='/gates')


@bp.route('', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def gates():
    if request.method == 'GET':
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 50)

        try:
            gates = Gate.objects.all().order_by('-created_time').skip(int(offset)).limit(int(limit))
            return make_response(gates.to_json())
        except:
            current_app.logger.exception('get gates failed')
            return abort(500)

    elif request.method == 'POST':
        pass
