from flask import Blueprint, request, make_response, jsonify
from app import jwt
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    jwt_optional,
    get_jwt_claims,
)
from app.mod_auth.models import User
from app.mod_auth.utils import admin_required

bp = Blueprint("mod_auth", __name__)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {"permissions": User.objects.get(username=identity).permissions}


@bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    try:
        User.objects.get(username=username, password=password)

    except User.DoesNotExist:
        return jsonify({"msg": "Bad username or password"}), 401

    except:
        return jsonify({"msg": "server error"}), 401

    else:
        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200


@bp.route("/protected", methods=["GET"])
@jwt_optional
def protected():
    current_user = get_jwt_identity()
    claims = get_jwt_claims()
    if current_user:
        return jsonify(logged_in_as=current_user, claims=claims), 200
    else:
        return jsonify(logged_in_as=None, claims=claims), 200


@bp.route("/admin-protected", methods=["GET"])
@admin_required
def admin_protected():
    return jsonify(secret_message="go banana!")
