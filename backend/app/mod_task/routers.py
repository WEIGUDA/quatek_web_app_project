from uuid import uuid1

from celerybeatmongo.models import PeriodicTask
from flask import (Blueprint, abort, current_app, jsonify, make_response,
                   request)
from mongoengine.queryset.visitor import Q


bp = Blueprint('mod_task', __name__)


@bp.route('/task-interval', methods=['GET', ])
def task_interval():
    if request.method == 'GET':
        tasks = PeriodicTask.objects.filter(interval__exists=True)
        return tasks.to_json(), {'Content-Type': 'application/json'}


@bp.route('/task-crontab', methods=['GET', ])
def task_crontab():
    if request.method == 'GET':
        tasks = PeriodicTask.objects.filter(crontab__exists=True)
        return tasks.to_json(), {'Content-Type': 'application/json'}


@bp.route('/task-interval-add-one', methods=['POST', ])
def task_interval_add_one():
    if request.method == 'POST':
        task = PeriodicTask(name=str(uuid1()), task=request.json['task'], enabled=True, run_immediately=True,
                            interval=PeriodicTask.Interval(every=int(request.json['every']), period='seconds'))
        result = task.save()
        return result.to_json(), {'Content-Type': 'application/json'}


@bp.route('/task-crontab-add-one', methods=['POST', ])
def task_crontab_add_one():
    if request.method == 'POST':
        task = PeriodicTask(
            name=str(uuid1()), task=request.json['task'], enabled=True,
            crontab=PeriodicTask.Crontab(
                minute=request.json['minute'],
                hour=request.json['hour'],
                day_of_month=request.json['day_of_month'],
                month_of_year=request.json['month_of_year'],
                day_of_week=request.json['day_of_week']))
        result = task.save()
        return result.to_json(), {'Content-Type': 'application/json'}


@bp.route('/task-delete', methods=['POST', ])
def task_delete():
    if request.method == 'POST':
        task = PeriodicTask.objects.get(pk=request.json['task_id'])
        result = task.delete()
        return task.to_json(), {'Content-Type': 'application/json'}

# @bp.route('/task', methods=['GET', ])
# def task():
#     if request.method == 'GET':
#         q = request.args.get('q', None)
#         tasks = PeriodicTask.objects.filter(task__icontains=q)
#         return tasks.to_json(), {'Content-Type': 'application/json'}
