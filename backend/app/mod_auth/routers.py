from flask import Blueprint, request, make_response, jsonify

bp = Blueprint('mod_auth', __name__, url_prefix='/auth')


@bp.route('/')
def default():
    response = make_response(jsonify({'result': 'from mod_auth'}))
    return response
