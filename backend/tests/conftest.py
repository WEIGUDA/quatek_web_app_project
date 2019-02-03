import os
import pytest
import pymongo

from app import create_app


@pytest.fixture(scope='module')
def client():
    # get configs fom environment
    os.environ['TESTING'] = 'True'
    os.environ['MONGODB_HOST'] = '127.0.0.1'
    os.environ['MONGODB_PORT'] = '27017'
    os.environ['MONGODB_DB'] = 'test_db'

    app = create_app()
    client = app.test_client()

    mongo_client = pymongo.MongoClient()
    test_db = mongo_client['test_db']
    test_collection = test_db['test_collection']
    test_collection.insert_one({'foo': 'bar'})

    yield client

    mongo_client.drop_database('test_db')
