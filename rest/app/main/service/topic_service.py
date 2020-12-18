import uuid
import datetime
from pymongo import MongoClient
from kafka import KafkaClient
from kafka.admin import KafkaAdminClient, NewTopic
import json
from ..util.mongo_helpers import get_mongo_conn

def create_new_topic(data):
    db = get_mongo_conn()
    schemas = db['schemas']
    topic_name = data['topic_name']
    brokers = ['kafka-topics-ui.109.225.89.133.xip.io:9092']
    num_partitions = data['num_partitions']
    replication_factor = data['replication_factor']

    data['topic_schema'] = json.loads(data['topic_schema'])
    print(data)
    key = {'topic_name': data['topic_name']}
    schemas.update(key, data, upsert=True)
    # schema_id = schemas.insert_one(data).inserted_id
    # print(schema_id)

    client = KafkaClient(bootstrap_servers=brokers)
    future = client.cluster.request_update()
    client.poll(future=future)
    metadata = client.cluster
    print(metadata.topics())
    if topic_name not in metadata.topics():
        admin_client = KafkaAdminClient(bootstrap_servers=brokers)

        topic_list = []
        topic_list.append(NewTopic(name=topic_name, num_partitions=num_partitions, 
                    replication_factor=replication_factor))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    
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
