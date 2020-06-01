from flask_restx import Namespace, fields

# Data Transfer Object (DTO) for marshalling data for our API calls

# DTO for User object
class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })

# DTO for authentication endpoint
class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

# DTO for Kafka topics
class TopicDto:
    api = Namespace('topic', description='Kafka topics related operations')
    topic = api.model('topic_details', {
        'topic_name': fields.String(required=True, description='Kafka Topic name'),
    })
