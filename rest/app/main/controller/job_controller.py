from flask import request
from flask_restx import Resource

from ..util.dto import JobDto
from ..service.job_service import get_all_jobs, create_new_job, get_job_by_id
from ..util.decorator import token_required

api = JobDto.api
_job = JobDto.job


@api.route('/submit')
class SubmitJob(Resource):
    @api.response(201, 'New Job Created.')
    @api.doc('create a new analytics job')
    @api.expect(_job, validate=True)
    @token_required
    def post(self):
        """Creates a new Analytics job """
        data = request.json
        return create_new_job(data=data)

@api.route('/list/all')
class JobInfoAll(Resource):
    @api.doc('List of jobs for the user')
    @api.marshal_list_with(_job, envelope='data')
    @token_required
    def get(self):
        """List all jobs"""
        return get_all_jobs()

    
@api.route('/list/<int:job_id>')
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
