from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage 

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

# DTO for Job object
class JobDto:
    api = Namespace('job', description='Analytics job related operations')
    job = api.model('job', {
        'job_name': fields.String(required=True, description='Job name'),
        'job_framework': fields.String(required=True, description='Framework to run the job on'),
        
    })
    job_upload_parser = api.parser()
    job_upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
    job_upload_parser.add_argument('framework', location='form', type=str, help="Framework for the job", required=True)
    job_upload_parser.add_argument('name', location='form', type=str, help="Name of the job", required=True)


# DTO for Quota object
class QuotaDto:
    api = Namespace('quota', description='Analytics job related operations')
    job = api.model('quota', {
        'job_name': fields.String(required=True, description='Job name'),
        'job_framework': fields.String(required=True, description='Framework to run the job on'),
    })