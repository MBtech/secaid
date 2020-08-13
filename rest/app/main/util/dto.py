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
        'topic_schema': fields.String(required=True, description='Kafka Topic Avro Schema'),
        'partitions': fields.Integer(1, description='Number of partitions for the Kafka topic'),
        'replication_factor': fields.Integer(1, description='Replication factor for the Kafka topic')
    })

    topic_list = api.model('topic_list', {
        'topic_names': fields.List(fields.String(description='Kafka Topic name'))
    })

    schema = api.model('topic_schema', {
        'topic_schema': fields.String(required=True, description='Kafka Topic Avro Schema'),
    })

# DTO for Job object
class JobDto:
    api = Namespace('job', description='Analytics job related operations')
    job = api.model('job', {
        'job_id': fields.String(required=True, description='Job Id'),
        'job_name': fields.String(required=True, description='Job name'),
        'job_framework': fields.String(required=True, description='Framework to run the job on'),
        
    })
    job_upload_parser = api.parser()
    job_upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
    job_upload_parser.add_argument('framework', location='form', type=str, help="Framework for the job", required=True)
    job_upload_parser.add_argument('name', location='form', type=str, help="Name of the job", required=True)
    job_upload_parser.add_argument('num_executors', location='form', type=int, help="Number of Executors", required=True)
    job_upload_parser.add_argument('executor_cores', location='form', type=int, help="Number of Cores per Executor", required=False, default=2)
    job_upload_parser.add_argument('executor_memory', location='form', type=str, help="Amount of memory per executor", required=False, default="4g")
    job_upload_parser.add_argument('driver_memory', location='form', type=str, help="Amount of memory for driver", required=False, default="4g")
    job_upload_parser.add_argument('driver_cores', location='form', type=int, help="Number of cores for driver", required=False, default=1)



# DTO for Quota object
class QuotaDto:
    api = Namespace('quota', description='Analytics job related operations')
    quota_info = api.model('quota', {
        'user_id': fields.String(required=True, description='User ID'),
        'core_hours_total': fields.Integer(required=True, description='Total Core Hours in Budget'),
        'core_hours_remaining': fields.Integer(required=True, description='Total Core Hours Remaining in the Budget'),
        'memory_hours_total': fields.Integer(required=True, description='Total Memory Hours in Budget'),
        'memory_hours_remaining': fields.Integer(required=True, description='Total Memory Hours Remaining in Budget'),
    })