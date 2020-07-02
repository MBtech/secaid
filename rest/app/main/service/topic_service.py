import uuid
import datetime
from pymongo import MongoClient
import json

def create_new_topic(data):
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
    schemas = db['schemas']
    topic_names = [x['topic_name'] for x in schemas.find()]
    response_object = {
        'topic_names': topic_names
    }
    return response_object, 200


def get_topic_schema(topic_name):
    print(topic_name)
    schemas = db['schemas']
    topic_schema = schemas.find_one({'topic_name': topic_name})['topic_schema']
    response_object = {
            'topic_schema' : topic_schema
        }
    return response_object, 200


config = json.load(open("config.json"))
mongo_host_ip = config["mongo_ip"]
mongo_host_port = config["mongo_port"]
username = config["mongo_username"]
password = config["mongo_password"]
database = config["database"]
client = MongoClient(host=mongo_host_ip, port=mongo_host_port,
                    username = username,
                    password = password,
                    authSource=database
                    )
db = client[database]