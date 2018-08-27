from uuid import uuid1

from celerybeatmongo.models import PeriodicTask
from flask import (Blueprint, abort, current_app, jsonify, make_response,
                   request)
from mongoengine.queryset.visitor import Q

from app.mod_system_config.models import SystemConfig


bp = Blueprint('mod_system_config', __name__)


@bp.route('/get-system-config', methods=['GET', ])
def get_system_config():
    try:
        system_config = SystemConfig.objects.get()
    except SystemConfig.DoesNotExist:
        system_config = SystemConfig()
        system_config.save()
    finally:
        return system_config.to_json(), {'Content-Type': 'application/json'}


@bp.route('/update-system-config', methods=['POST', ])
def update_system_config():
    system_config = SystemConfig.objects.get()
    system_config.smtp_host = request.json['smtp_host']
    system_config.smtp_port = int(request.json['smtp_port'])
    system_config.smtp_username = request.json['smtp_username']
    system_config.smtp_password = request.json['smtp_password']
    system_config.smtp_use_ssl = request.json['smtp_use_ssl']
    system_config.smtp_use_tls = request.json['smtp_use_tls']
    system_config.emails = request.json['emails']
    system_config.work_hours = request.json['work_hours']

    system_config.save()

    return system_config.to_json(), {'Content-Type': 'application/json'}
