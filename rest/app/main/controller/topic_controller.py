from flask import request
from flask_restx import Resource

from ..util.dto import TopicDto
from ..service.topic_service import get_all_topics, create_new_topic, get_topic_schema
from ..util.decorator import token_required

api = TopicDto.api
_topic = TopicDto.topic
_schema = TopicDto.schema
_topic_names = TopicDto.topic_list


@api.route('/')
class TopicList(Resource):
    @api.doc('list of available topics')
    @api.marshal_with(_topic_names)
    @token_required
    def get(self):
        """List all available topics"""
        return get_all_topics()

@api.route('/create')
class CreateTopic(Resource):
    @api.response(201, 'New Kafka topic Created.')
    @api.doc('create a new Kafka topic')
    @api.expect(_topic, validate=True)
    @token_required
    def post(self):
        """Creates a new Kafka Topic """
        data = request.json
        return create_new_topic(data=data)

@api.route('/<string:topic_name>/schema')
@api.param('topic_name', 'Topic name')
@api.response(404, 'Topic not found.')
class GetSchema(Resource):    
    @api.response(201, 'Topic Schema returned.')
    @api.doc('return the schema of a kafka topic')
    # @api.marshal_with(_schema, envelope='data')
    @token_required
    def get(self, topic_name):
        """ Return the scheme of a kafka topic """
        return get_topic_schema(topic_name)
