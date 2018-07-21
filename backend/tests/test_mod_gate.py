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
        pass

    yield client

    mongo_client = MongoClient(app.config['MONGODB_SETTINGS']['host'],
                               app.config['MONGODB_SETTINGS']['port'])
    mongo_client.drop_database(app.config['MONGODB_SETTINGS']['db'])


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


def test_cardtests_search_with_no_query_string(client):
    """ GIVEN 120 cardtests, 1 cardtest/min
        WHEN query with datetime_from and datetime_to, without query_string
        THEN check returned cardtests lengths
    """
    dt = datetime.datetime.utcnow()
    for i in range(120):
        cardtest = CardTest(gate_number='cardtest' + str(i),
                            test_datetime=dt + datetime.timedelta(minutes=i),
                            job_number='jobnumber' + str(i)
                            )
        cardtest.save()

    now = datetime.datetime.utcnow()
    datetime_from = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    datetime_to = (now + datetime.timedelta(minutes=40)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    rv = client.get('/cardtests?datetime_from={}&datetime_to={}'.format(datetime_from, datetime_to))
    cardtests1 = json.loads(rv.data.decode())

    datetime_from = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    datetime_to = (dt + datetime.timedelta(minutes=40)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    rv = client.get('/cardtests?datetime_from={}&datetime_to={}'.format(datetime_from, datetime_to))
    cardtests2 = json.loads(rv.data.decode())

    assert len(cardtests1) == 40
    assert len(cardtests2) == 41


def test_cardtests_search_with_query_string(client):
    """ GIVEN 120 cardtests, 1 cardtest/min
        WHEN query with datetime_from, datetime_to and query_string
        THEN check returned cardtests lengths
    """
    dt = datetime.datetime.utcnow()

    for i in range(120):
        cardtest = CardTest(gate_number='cardtest' + str(i),
                            test_datetime=dt + datetime.timedelta(minutes=i),
                            job_number='jobnumber' + str(i)
                            )
        cardtest.save()

    now = datetime.datetime.utcnow()
    datetime_from = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    datetime_to = (now + datetime.timedelta(minutes=40)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    query_string1 = 'cardtest19'

    rv1 = client.get('/cardtests?datetime_from={}&datetime_to={}&q={}'.format(datetime_from, datetime_to, query_string1))
    cardtests1 = json.loads(rv1.data.decode())
    assert len(cardtests1) == 1

    query_string2 = 'cardtest0'

    rv2 = client.get('/cardtests?datetime_from={}&datetime_to={}&q={}'.format(datetime_from, datetime_to, query_string2))
    cardtests2 = json.loads(rv2.data.decode())
    assert len(cardtests2) == 0


# def test_json(client):
#     rv = client.post('/', json={
#         'username': 'flask', 'password': 'secret'
#     })
#     json_data = rv.get_json()
#     assert json_data == json_data
