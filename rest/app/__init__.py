from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.topic_controller import api as topic_ns
from .main.controller.job_controller import api as job_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='SECAID REST SERVER BOILER-PLATE WITH JWT',
          version='0.1a',
          description='a boilerplate for se-caid rest server'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(topic_ns)
api.add_namespace(job_ns)