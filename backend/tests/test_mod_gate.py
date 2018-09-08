import datetime
import json
import os
import random
from pprint import pprint

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


@pytest.fixture
def create_cardtest_list():
    dt = datetime.datetime.utcnow()
    cardtest_list = []
    for i in range(500):
        cardtest_list.append(CardTest(log_id=f'id{i}', card_counter=f'{i}', card_number=f'number{i}', card_category=random.choice(['0', '1', '2', '3']), in_out_symbol=random.choice(['0', '1']), mc_id=random.choice(['mc1', 'mc2']), test_datetime=dt+timedelta(
            minutes=i), test_result=random.choice(['0', '1']), is_tested=random.choice(['0', '1']), hand=str(random.randrange(0, 100000)), left_foot=str(random.randrange(0, 100000)), right_foot=str(random.randrange(0, 100000))))
    CardTest.objects.insert(cardtest_list)
    yield cardtest_list


@pytest.fixture
def create_card_list():
    card_list = []
    for i in range(1000):
        card_list.append(Card(card_number=hex(random.randint(0, 4294967295))[2:].upper().rjust(
            8, '0'), card_category=random.choice(['0', '1', '2', '3']), name=f'name{i}', job_number=random.randint(1, 9999999999), department=f'部门{i}', gender=random.choice(['0', '1']), note='default note', belong_to_mc='all', ))
    Card.objects.insert(card_list)
    yield card_list


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


def test_cardtests_search_with_query_string(client):
    """ GIVEN 120 cardtests, 
        WHEN query with datetime_from, datetime_to and query_string
        THEN check returned cardtests lengths
    """

    dt = datetime.datetime.utcnow()
    cardtests = []

    gate = Gate(mc_id='mc_id_3', name='gate3')
    gate.save()

    for i in range(60):
        cardtest = CardTest(
            card_number='card_number_{}'.format(i),
            test_datetime=dt + datetime.timedelta(minutes=i),
            job_number='job_number_{}'.format(i),
            mc_id='mc_id_3'
        )
        cardtests.append(cardtest)

    for i in range(60, 120):
        cardtest = CardTest(
            card_number='card_number_{}'.format(i),
            test_datetime=dt + datetime.timedelta(minutes=i),
            job_number='job_number_{}'.format(i),
            mc_id='mc_id_4'
        )
        cardtests.append(cardtest)

    CardTest.objects.insert(cardtests)

    now = datetime.datetime.utcnow()
    datetime_from = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    datetime_to = (now + datetime.timedelta(minutes=120)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    query_string1 = 'card_number_19'
    rv1 = client.get('/cardtests?datetime_from={}&datetime_to={}&q={}'
                     .format(datetime_from, datetime_to, query_string1))
    cardtests1 = json.loads(rv1.data.decode())
    assert len(cardtests1) == 1

    query_string2 = 'gate3'
    rv2 = client.get('/cardtests?datetime_from={}&datetime_to={}&q={}'
                     .format(datetime_from, datetime_to, query_string2))
    cardtests2 = json.loads(rv2.data.decode())
    assert len(cardtests2) == 50

    query_string3 = ''
    rv3 = client.get('/cardtests?datetime_from={}&datetime_to={}&q={}'
                     .format(datetime_from, datetime_to, query_string3))
    cardtests3 = json.loads(rv3.data.decode())
    assert len(cardtests3) == 50
