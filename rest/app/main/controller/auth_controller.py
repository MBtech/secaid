from flask import request
from flask_restx import Resource

# from app.main.service.auth_helper import Auth
from app.main.service.user_service import *
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth
user = AuthDto.user


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return login(data=post_data)

@api.route('/register')
class UserRegister(Resource):
    """
        User Register Resource
    """
    @api.doc('user register')
    @api.expect(user, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return register(data=post_data)

@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return logout()