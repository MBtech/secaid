import uuid
import datetime
import json
from pymongo import MongoClient

from app.main import db
from app.main.model.user import User


def get_quota_info(data):
    # Access quota collection
    quotas = db['quotas']
    user_quota_info = quotas.find_one({"id": data["user_id"]})
    return user_quota_info, 200
    # response_object = {
    #         'status': 'Success',
    #         'message': 'This stub is empty at the moment',
    #     }
    # return response_object, 200

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            # public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


config = json.load(open("config.json"))
mongo_host_ip = config["mongo_ip"]
mongo_host_port = config["mongo_port"]
username = config["mongo_username"]
password = config["mongo_password"]
database = config["database"]
client = MongoClient(host=mongo_host_ip, port=mongo_host_port,
                    # username = username,
                    # password = password,
                    # authSource=database
                    )
db = client[database]