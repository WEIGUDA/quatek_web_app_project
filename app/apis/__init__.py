from flask import Blueprint
from flask import request
from flask import jsonify

from flask_restful import Api, Resource
from mongoengine.queryset.visitor import Q, QCombination

from app.models.user import User
from app.models.machine import Machine
from app.models.card import Card
from app.models.static import StaticTest
from app.models.attendance import Attendance

