import uuid
import datetime
from multiprocessing import Process
from livy import LivyBatch


from app.main import db

# TODO: This needs to be configurable
LIVY_URL = "http://localhost:8998"

def submit_job(data):
    batch = LivyBatch.create(
        url=LIVY_URL,
        file=data["file"],
        executor_cores=data["executor_cores"],
        executor_memory=data["executor_memory"],
        driver_cores=data["driver_cores"],
        driver_memory=data["driver_memory"],
        num_executors=data["num_executors"]
    )
    batch.wait()
    ## How do we get the execution time of the job?
    ## Request to Spark history server or by measuring the time here?

    

def create_new_job(data):
    ## Currently done with multiprocessing but if high traffic is expected it should be Celery with RabbitMQ and Redis
    job = Process(target=submit_job, daemon=True, args=(data))
    job.start()
    response_object = {
            'status': 'Success',
            'message': 'The job has been submitted',
        }
    return response_object, 200


def get_all_jobs():
    response_object = {
            'status': 'Success',
            'message': 'This stub is empty at the moment',
        }
    return response_object, 200

def get_job_by_id(job_id):
    response_object = {
            'status': 'Success',
            'message': 'This stub is empty at the moment',
        }
    return response_object, 200

def save_changes(data):
    db.session.add(data)
    db.session.commit()