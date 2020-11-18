import uuid
import datetime
from pymongo import MongoClient
import json
from ..util.mongo_helpers import get_mongo_conn

def create_new_topic(data):
    db = get_mongo_conn()
    schemas = db['schemas']
    data['topic_schema'] = json.loads(data['topic_schema'])
    print(data)
    schema_id = schemas.insert_one(data).inserted_id
    print(schema_id)
    response_object = {
            'status': 'Success',
            'message': 'Topic has been created',
        }
    return response_object, 200


def get_all_topics():
    db = get_mongo_conn()
    schemas = db['schemas']
    topic_names = [x['topic_name'] for x in schemas.find()]
    response_object = {
        'topic_names': topic_names
    }
    return response_object, 200


def get_topic_schema(topic_name):
    db = get_mongo_conn()
    print(topic_name)
    schemas = db['schemas']
    topic_schema = schemas.find_one({'topic_name': topic_name})['topic_schema']
    response_object = {
            'topic_schema' : topic_schema
        }
    return response_object, 200
