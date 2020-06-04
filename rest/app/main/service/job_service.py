import uuid
import datetime

from app.main import db

def create_new_job(data):
    response_object = {
            'status': 'Success',
            'message': 'This stub is empty at the moment',
        }
    return response_object, 200


def get_all_jobs():
    response_object = {
            'status': 'Success',
            'message': 'This stub is empty at the moment',
        }
    return response_object, 200

def get_job_by_id(job_id):
    response_object = {
            'status': 'Success',
            'message': 'This stub is empty at the moment',
        }
    return response_object, 200

def save_changes(data):
    db.session.add(data)
    db.session.commit()