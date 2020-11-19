from flask import request, session, send_from_directory
from flask_restx import Resource
import os 

from ..util.dto import JobDto
from ..service.job_service import get_all_jobs, create_new_job, get_logs_by_id, submit_job, get_results_by_id
from ..util.decorator import token_required
from ..util.keycloak_utils import get_userinfo

api = JobDto.api
_job = JobDto.job
job_parser = JobDto.job_upload_parser


@api.route('/submit')
class SubmitJob(Resource):
    @api.response(201, 'New Job Created.')
    @api.doc('create a new analytics job')
    @api.expect(job_parser, validate=True)
    @token_required
    def post(self):
        """Creates a new Analytics job """
        access_token = session.get('access_token')
        userinfo = get_userinfo(access_token)
        # print(userinfo)
        user_id = userinfo["sub"]
        print(user_id)
        data = job_parser.parse_args()
        print(data)
        # return submit_job(**data)
        return create_new_job(user_id, **data)

@api.route('/info')
class JobInfoAll(Resource):
    @api.doc('List of jobs for the user')
    @api.marshal_list_with(_job, envelope='data')
    @token_required
    def get(self):
        """List all jobs"""
        access_token = session.get('access_token')
        userinfo = get_userinfo(access_token)
        # print(userinfo)
        user_id = userinfo["sub"]
        # print(userid)
        return get_all_jobs(user_id)

    
@api.route('/<string:job_id>/log')
@api.param('job_id', 'The Job identifier')
@api.response(404, 'Job not found.')
class JobLog(Resource):
    @api.doc('Retrieve job logs by Id')
    # @api.marshal_with(_job)
    @token_required
    def get(self, job_id):
        """Retrieve job logs by Id"""
        access_token = session.get('access_token')
        userinfo = get_userinfo(access_token)
        user_id = userinfo["sub"]
        job_logs, response_code = get_logs_by_id(user_id, job_id)

        if job_logs['filename'] == None:
            return {'message': 'Job not found'}, 404

        try:
            return send_from_directory('../../../logs', job_logs['filename'], as_attachment=True)
        except FileNotFoundError:
            return {'message': 'File not found'}, 404



@api.route('/<string:job_id>/result')
@api.param('job_id', 'The Job identifier')
@api.response(404, 'Job not found.')
class JobResult(Resource):
    @api.doc('Retrieve job result by Job Id')
    @api.marshal_with(_job)
    @token_required
    def get(self, job_id):
        """Retrieve job result by Job ID"""
        access_token = session.get('access_token')
        userinfo = get_userinfo(access_token)
        user_id = userinfo["sub"]

        job_info = get_results_by_id(user_id, job_id)
        if not job_info:
            api.abort(404)
        else:
            return job_info