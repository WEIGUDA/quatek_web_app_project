from uuid import uuid1

from celerybeatmongo.models import PeriodicTask
from flask import (Blueprint, abort, current_app, jsonify, make_response,
                   request)
from mongoengine.queryset.visitor import Q
import flask_excel as excel

from app.mod_system_config.models import SystemConfig
from app.mod_system_config.utils import convertor1


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
    system_config.smtp_need_auth = request.json['smtp_need_auth']

    system_config.save()

    return system_config.to_json(), {'Content-Type': 'application/json'}


@bp.route('/get-other-database-config', methods=['GET', ])
def get_other_database_config():
    try:
        system_config = SystemConfig.objects.get()
    except SystemConfig.DoesNotExist:
        system_config = SystemConfig()
        system_config.save()
    finally:
        return system_config.to_json(), {'Content-Type': 'application/json'}


@bp.route('/update-other-database-config', methods=['POST', ])
def update_other_database_config():
    system_config = SystemConfig.objects.get()
    system_config.db_type = request.json['db_type']
    system_config.db_name = request.json['db_name']
    system_config.db_host = request.json['db_host']
    system_config.db_port = int(request.json['db_port'])
    system_config.db_username = request.json['db_username']
    system_config.db_password = request.json['db_password']
    system_config.save()

    return system_config.to_json(), {'Content-Type': 'application/json'}


@bp.route('/hid_card_convertor', methods=['POST', ])
def hid_card_convertor():
    card_number_list = request.get_array(field_name='hid_excel_file')
    for row_list in card_number_list:
        row_list.append(convertor1(row_list[0]))
    return excel.make_response_from_array(card_number_list, 'xlsx',)
