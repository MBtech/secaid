import uuid
import datetime
import json
import logging
from pymongo import MongoClient

from app.main import db
# from app.main.model.user import User

from flask import Flask, request, render_template, redirect, flash, url_for
from flask import session, make_response, g
from flask import current_app

from ..util.keycloak_utils import get_admin, create_user, get_oidc, get_token, check_token

# from ..util.mongo_helpers import get_mongo_conn

# logging.basicConfig(level=logging.DEBUG)

# @app.before_request
def load_user():
    g.username = session.get('username')
    g.access_token = session.get('access_token')


def login(data):
    oidc_obj = get_oidc()
    token = get_token(oidc_obj, data["username"], data["password"])
    print("\nTOKEN: %s\n" % token)

    if token:
        
        session['access_token'] = token['access_token']
        session['username'] = data["username"]
        response_object = {
            'status': 'success',
            'message': 'Successfully logged in'
        }
        response = make_response(response_object, 201)
        response.set_cookie('access_token', token['access_token'])
        return response
    response_object = {
            'status': 'failed',
            'message': 'User not found'
        }    
    return response_object, 409

def logout():
    session.pop('username', None)
    session.pop('access_token', None)
    response_object = {
            'status': 'success',
            'message': 'Successfully logged out'
        }
    return response_object, 201


def register(data):
    admin = get_admin()
    
    create_user(admin, data["username"], 
            data["email"], data["password"],
            data["organization"]
            )
    flash('Thanks for registering')
    response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
    return response_object, 201


# @app.route('/headers')
def headers():
    return dict(request.headers)


# @app.route('/protected')
# def protected():
#     ingress_host = current_app.config.get('INGRESS_HOST')
#     resp = 'Forbidden!'
#     access_token = session.get('access_token')
#     if access_token:
#         if check_token(access_token):
#             headers = {'Authorization': 'Bearer ' + access_token}
#             r = requests.get(ingress_host, headers=headers)
#             resp = 'Protected resource is accessible. Yay! Here is the response: %s' % str(r.text)
#     return resp


# def get_quota_info(data):
#     # Access quota collection
#     quotas = db['quotas']
#     user_quota_info = quotas.find_one({"id": data["user_id"]})
#     return user_quota_info, 200
#     # response_object = {
#     #         'status': 'Success',
#     #         'message': 'This stub is empty at the moment',
#     #     }
#     # return response_object, 200

# def save_new_user(data):
#     user = User.query.filter_by(email=data['email']).first()
#     if not user:
#         new_user = User(
#             # public_id=str(uuid.uuid4()),
#             email=data['email'],
#             username=data['username'],
#             password=data['password'],
#             registered_on=datetime.datetime.utcnow()
#         )
#         save_changes(new_user)
#         return generate_token(new_user)
#     else:
#         response_object = {
#             'status': 'fail',
#             'message': 'User already exists. Please Log in.',
#         }
#         return response_object, 409


# def get_all_users():
#     return User.query.all()


# def get_a_user(public_id):
#     return User.query.filter_by(public_id=public_id).first()


# def save_changes(data):
#     db.session.add(data)
#     db.session.commit()


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
