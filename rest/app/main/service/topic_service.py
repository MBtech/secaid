import uuid
import datetime

from app.main import db

def create_new_topic(data):
    response_object = {
            'status': 'Success',
            'message': 'This stub is empty at the moment',
        }
    return response_object, 200


def get_all_topics():
    response_object = {
            'status': 'Success',
            'message': 'This stub is empty at the moment',
        }
    return response_object, 200


def get_topic_schema(topic_name):
    response_object = {
            'status': 'Success',
            'message': 'This stub is empty at the moment',
        }
    return response_object, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()