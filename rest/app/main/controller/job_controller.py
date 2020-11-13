from flask import request, session
from flask_restx import Resource

from ..util.dto import JobDto
from ..service.job_service import get_all_jobs, create_new_job, get_job_by_id, submit_job
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
        userid = userinfo["sub"]
        print(userid)
        data = job_parser.parse_args()
        print(data)
        # return submit_job(**data)
        return create_new_job(userid, **data)

@api.route('/info')
class JobInfoAll(Resource):
    @api.doc('List of jobs for the user')
    @api.marshal_list_with(_job, envelope='data')
    @token_required
    def get(self):
        """List all jobs"""
        return get_all_jobs()

    
@api.route('/<int:job_id>/info')
@api.param('job_id', 'The Job identifier')
@api.response(404, 'Job not found.')
class JobInfo(Resource):
    @api.doc('Retrieve job info by Id')
    @api.marshal_with(_job)
    @token_required
    def get(self, job_id):
        """Retrieve job info by Id"""
        job_info = get_job_by_id(job_id)
        if not job_info:
            api.abort(404)
        else:
            return job_info

@api.route('/<int:job_id>/result')
@api.param('job_id', 'The Job identifier')
@api.response(404, 'Job not found.')
class JobInfo(Resource):
    @api.doc('Retrieve job result by Job Id')
    @api.marshal_with(_job)
    @token_required
    def get(self, job_id):
        """Retrieve job result by Job ID"""
        job_info = get_job_by_id(job_id)
        if not job_info:
            api.abort(404)
        else:
            return job_info