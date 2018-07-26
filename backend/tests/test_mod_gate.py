import datetime
import json
import os

import pytest
from pymongo import MongoClient

from app import create_app
from app.mod_auth.models import User
from app.mod_gate.models import Card, CardTest, Gate


@pytest.fixture
def client():
    app = create_app(config='config_test.py')
    client = app.test_client()

    with app.app_context():
        # init database
        pass

    yield client

    mongo_client = MongoClient(app.config['MONGODB_HOST'],
                               app.config['MONGODB_PORT'])
    mongo_client.drop_database(app.config['MONGODB_DB'])


def test_gates_filter(client):
    for i in range(10):
        gate = Gate(name='gate1_' + str(i), category='category1')
        gate.save()

    for i in range(10):
        gate = Gate(name='gate2_' + str(i), category='category2')
        gate.save()

    rv = client.get('/gates?q=category1')
    gates = json.loads(rv.data.decode())
    assert len(gates) == 10


def test_cardtests_search_with_query_string2(client):
    """ GIVEN 120 cardtests, 
        WHEN query with datetime_from, datetime_to and query_string
        THEN check returned cardtests lengths
    """

    dt = datetime.datetime.utcnow()

    gate = Gate(mc_id='mc_id_2', name='gate3')
    gate.save()

    for i in range(60):
        cardtest = CardTest(
            card_number='card_number_{}'.format(i),
            test_datetime=dt + datetime.timedelta(minutes=i),
            job_number='job_number_{}'.format(i),
            mc_id='mc_id_1'
        )
        cardtest.save()

    for i in range(60, 120):
        cardtest = CardTest(card_number='card_number_{}'.format(i),
                            test_datetime=dt + datetime.timedelta(minutes=i),
                            job_number='job_number_{}'.format(i),
                            mc_id='mc_id_2'
                            )
        cardtest.save()

    now = datetime.datetime.utcnow()
    datetime_from = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    datetime_to = (now + datetime.timedelta(minutes=120)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    query_string1 = 'card_number_19'
    rv1 = client.get('/cardtests?datetime_from={}&datetime_to={}&q={}'.format(datetime_from, datetime_to, query_string1))
    cardtests1 = json.loads(rv1.data.decode())
    assert len(cardtests1) == 1

    query_string2 = 'gate3'
    rv2 = client.get('/cardtests?datetime_from={}&datetime_to={}&q={}'.format(datetime_from, datetime_to, query_string2))
    cardtests2 = json.loads(rv2.data.decode())
    assert len(cardtests2) == 60


# def test_json(client):
#     rv = client.post('/', json={
#         'username': 'flask', 'password': 'secret'
#     })
#     json_data = rv.get_json()
#     assert json_data == json_data
