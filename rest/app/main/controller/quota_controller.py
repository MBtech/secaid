from flask import request
from flask_restx import Resource

from ..util.dto import QuotaDto
from ..service.quota_service import get_quota_info

api = QuotaDto.api
_quota_info = QuotaDto.quota_info


@api.route('/<string:user_id>/schema')
@api.param('user_id', 'User ID')
@api.response(404, 'User not found.')
class GetSchema(Resource):    
    @api.response(201, 'Quota Information Returned')
    @api.doc('return the quota information of a user')
    @api.marshal_with(_quota_info, envelope='data')
    # @token_required
    def get(self, user_id):
        """ Return the quota information of a user """
        return get_quota_info(user_id)