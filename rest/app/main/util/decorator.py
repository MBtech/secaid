from functools import wraps
from flask import request, session

from app.main.service.auth_helper import Auth
from ..util.keycloak_utils import check_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = session.get('access_token')
        if not access_token or not check_token(access_token):
            response_object = {
            'status': 'fail',
            'message': 'Not Logged in. Please Login first'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated

# TODO: Update this for keycloak case as well
def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated