from flask import request
from flask_restx import Resource

from ..util.dto import DatasetDto
from ..service.dataset_service import get_all_datasets, get_dataset_schema
from ..util.decorator import token_required

api = DatasetDto.api
_schema = DatasetDto.schema
_dataset_names = DatasetDto.dataset_list

@api.route('/list')
class DatasetList(Resource):
    @api.doc('list of available topics')
    @api.marshal_with(_dataset_names)
    @token_required
    def get(self):
        """List all available dataset"""
        return get_all_datasets()

@api.route('/<string:dataset_name>/schema')
@api.param('dataset_name', 'Dataset name')
@api.response(404, 'dataset not found.')
class GetSchema(Resource):    
    @api.response(201, 'Dataset Schema returned.')
    @api.doc('return the schema of a dataset')
    @api.marshal_with(_schema, envelope='data')
    @token_required
    def get(self, dataset_name):
        """ Return the scheme of a dataset """
        return get_dataset_schema(dataset_name)
