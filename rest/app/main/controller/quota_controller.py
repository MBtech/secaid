from flask import request, session
from flask_restx import Resource

from ..util.dto import QuotaDto
from ..util.decorator import token_required
from ..service.quota_service import get_quota_info
from ..util.keycloak_utils import get_userinfo

api = QuotaDto.api
_quota_info = QuotaDto.quota_info


@api.route('/')
@api.response(404, 'Quota information not found.')
class GetSchema(Resource):    
    @api.response(201, 'Quota Information Returned')
    @api.doc('return the quota information of a user')
    @api.marshal_with(_quota_info, envelope='data')
    @token_required
    def get(self):
        """ Return the quota information of a user """
        access_token = session.get('access_token')
        userinfo = get_userinfo(access_token)
        # print(userinfo)
        userid = userinfo["sub"]
        # print(userid)
        return get_quota_info(userid)