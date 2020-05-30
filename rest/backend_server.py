from flask import Flask
from flask_restx import Api, Resource
import flask 

flask_app = Flask(__name__)
app = Api(app=flask_app)

namespace = app.namespace('portal/v1', description='Main APIs')

@namespace.route("/login")
class Login(Resource):
    def post(self, id):
        return "User login logic goes here"

@namespace.route("/signup")
class Signup(Resource):
    def post(self, id):
        return "User signup logic goes here"

@namespace.route('/topics')
class Topics(Resource):
    def get(self, topic_id):
        return "Return the topic list as json"
    def post(self, topic_id):
        return "Create a topic"

@namespace.route('/datasets')
class Datasets(Resource):
    def get(self, dataset_id):
        return "Return a list of the available datasets and their metadata as json"

@namespace.route('/quota')
class Quota(Resource):
    def get(self, id):
        return "Return quota information"

@namespace.route('/job')
class Job(Resource):
    def post(self, job_id):
        return "Submit a job"


@namespace.route('/result')
class Results(Resource):
    def get(self, job_id):
        return "Return the results of a job based on the job id"

if __name__ == '__main__':
    flask_app.run(debug=True)