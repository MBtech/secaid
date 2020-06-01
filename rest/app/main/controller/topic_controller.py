from flask import request
from flask_restx import Resource

from ..util.dto import TopicDto
from ..service.topic_service import get_all_topics, create_new_topic
from ..util.decorator import token_required

api = TopicDto.api
_topic = TopicDto.topic


@api.route('/')
class UserList(Resource):
    @api.doc('list of available topics')
    @api.marshal_list_with(_topic, envelope='data')
    def get(self):
        """List all available topics"""
        return get_all_topics()

    @api.response(201, 'New Kafka topic Created.')
    @api.doc('create a new Kafka topic')
    @api.expect(_topic, validate=True)
    def post(self):
        """Creates a new Kafka Topic """
        data = request.json
        return create_new_topic(data=data)
