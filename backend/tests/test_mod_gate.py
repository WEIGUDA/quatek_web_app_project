import os
import pytest
import datetime
import json
from pymongo import MongoClient

from app import create_app
from app.mod_gate.models import Gate, Card, CardTest
from app.mod_auth.models import User


TEST_CONFIG = {'ENV': 'test',
               'DEBUG': False,
               'TESTING': True,
               'SECRET_KEY': os.urandom(24),
               'MONGODB_SETTINGS': {
                   'db': 'quatek_web_app_test',
                   'host': '127.0.0.1',
                   'port': 27017,
               },
               #    'CELERY_RESULT_BACKEND': 'redis://localhost:6379',
               #    'CELERY_BROKER_URL': 'redis://localhost:6379'
               }


@pytest.fixture
def client():
    app = create_app(config=TEST_CONFIG)
    client = app.test_client()

    with app.app_context():
        # init database
        dt = datetime.datetime.utcnow()
        for i in range(100):
            cardtest = CardTest(gate_number='cardtest' + str(i),
                                test_datetime=dt + datetime.timedelta(minutes=i * 10),
                                job_number='jobnumber' + str(i)
                                )
            cardtest.save()

    yield client

    mongo_client = MongoClient(TEST_CONFIG['MONGODB_SETTINGS']['host'], TEST_CONFIG['MONGODB_SETTINGS']['port'])
    mongo_client.drop_database(TEST_CONFIG['MONGODB_SETTINGS']['db'])


def test_cardtests_search(client):
    now = datetime.datetime.utcnow()
    datetime_from = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    datetime_to = (now + datetime.timedelta(hours=5)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    r = client.get('/cardtests?datetime_from={}&datetime_to={}'.format(datetime_from, datetime_to))
    cardtests = json.loads(r.data.decode())

    assert len(cardtests) == 30
