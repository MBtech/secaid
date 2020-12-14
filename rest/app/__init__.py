from flask_restx import Api
from flask import Blueprint

# from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.topic_controller import api as topic_ns
from .main.controller.job_controller import api as job_ns
from .main.controller.quota_controller import api as quota_ns
from .main.controller.dataset_controller import api as dataset_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='SECAID REST SERVER',
          version='0.1a',
          description='A WIP backend rest server for SE-CAID' 
          )

# api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(topic_ns)
api.add_namespace(job_ns)
api.add_namespace(quota_ns)
api.add_namespace(dataset_ns)