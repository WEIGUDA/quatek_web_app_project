import os
import pytest
import datetime
import json
from pymongo import MongoClient

from app import create_app
from app.mod_gate.models import Gate, Card, CardTest
from app.mod_auth.models import User


@pytest.fixture
def client():
    app = create_app(config='config_test.py')
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

    mongo_client = MongoClient(app.config['MONGODB_SETTINGS']['host'],
                               app.config['MONGODB_SETTINGS']['port'])
    mongo_client.drop_database(app.config['MONGODB_SETTINGS']['db'])


def test_cardtests_search(client):
    now = datetime.datetime.utcnow()
    datetime_from = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    datetime_to = (now + datetime.timedelta(hours=5)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    rv = client.get('/cardtests?datetime_from={}&datetime_to={}'.format(datetime_from, datetime_to))
    cardtests = json.loads(rv.data.decode())

    assert len(cardtests) == 30


# def test_json(client):
#     rv = client.post('/', json={
#         'username': 'flask', 'password': 'secret'
#     })
#     json_data = rv.get_json()
#     assert json_data == json_data
