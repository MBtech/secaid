from flask import Flask
import flask 

app = Flask(__name__)

@app.route('/')
def index():
    return "Use one of the documented endpoints"

@app.route('/portal/v1/login', methods=['POST'])
def login():
    return "User login logic goes here"

@app.route('/portal/v1/signup', methods=['POST'])
def signup():
    return "User login logic goes here"

@app.route('/portal/v1/topics', methods=['GET', 'POST'])
def topics():
    if flask.request.method == 'GET':
        return "Return the topic list as json"
    else:
        return "Create a topic"

@app.route('/portal/v1/datasets', methods=['GET'])
def datasets():
    return "Return a list of the available datasets and their metadata as json"

@app.route('/portal/v1/quota', methods=['GET'])
def quota():
    return "Return quota information"

@app.route('/portal/v1/job', methods=['POST'])
def job():
    return "Submit a job"

@app.route('/portal/v1/result', methods=['GET'])
def result():
    return "Return the results of a job based on the job id"

if __name__ == '__main__':
    app.run(debug=True)