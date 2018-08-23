from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

bp = Blueprint('mod_auth', __name__,)


@bp.route('/auth')
def default():
    response = make_response(jsonify({'result': 'from mod_auth'}))
    return response


@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'desmond' or password != 'weiguda':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
