import uuid
import datetime
from multiprocessing import Process, Queue
from livy import LivyBatch
from pymongo import MongoClient
import requests
import json
import os 

from flask import current_app

from ..util.helpers import get_consumed_resources, available_quota
from ..util.mongo_helpers import get_mongo_conn

from app.main import db

# TODO: This needs to be configurable
# LIVY_URL = "http://localhost:8998"
LIVY_URL = "http://livy.se-caid.org"
history_server_url = "https://history.se-caid.org"
# Create the logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

def submit_job(userid, **data):
    try:
        batch = LivyBatch.create(
        url=LIVY_URL,
        file=data["file"],
        py_files=data["py_files"],
        class_name=data["class_name"],
        jars=data["jars"],
        verify=False,
        executor_cores=data["executor_cores"],
        executor_memory=data["executor_memory"],
        driver_cores=data["driver_cores"],
        driver_memory=data["driver_memory"],
        num_executors=data["num_executors"],
        spark_conf= {
                "spark.kubernetes.namespace": "spark-cluster",
                "spark.kubernetes.driver.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.mount.path": "/data",
                "spark.kubernetes.driver.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.mount.readOnly": False,
                "spark.kubernetes.driver.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.options.claimName":"events-dir",
                "spark.kubernetes.executor.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.mount.path": "/data",
                "spark.kubernetes.executor.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.mount.readOnly": False,
                "spark.kubernetes.executor.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.options.claimName":"events-dir"
            }
        )
        
        batch.wait()
        # batch.batch_id
        b = batch.client.get_batch(batch.batch_id)
        jobid = b.app_id
        print(jobid)
        print(batch.state)
        with open(jobid+".log", 'w') as f:
            f.writelines(batch.log())
            
    except:
        print("An exception has occurred. Terminating the call")
        # return -1 
        jobid = "1"

    
    r = requests.get(history_server_url + "/api/v1/applications/"+jobid, verify=False)
    job_json_data = r.json()
    ## What if jobs in the application fails
    job_runtime = job_json_data["attempts"][0]["duration"]/1000.0

    db = get_mongo_conn()
    userinfo_col = db['userinfo']
    ret = userinfo_col.find_one({'id': userid})
    print(ret)
    if ret == None:
        # Change the defaults here and pull them from a config file instead
        userinfo_col.insert_one({
                        'id': userid,
                        'jobs': [],
                        'remaining_quota':  {'cpu_hours': current_app.config.get('QUOTA_CPU_HOURS'),
                                             'memory_hours': current_app.config.get('QUOTA_MEMORY_HOURS')},
                        'total_quota': {'cpu_hours': current_app.config.get('QUOTA_CPU_HOURS'),
                                         'memory_hours': current_app.config.get('QUOTA_MEMORY_HOURS')}
                        })
        ret = userinfo_col.find_one({'id': userid})

    ret['jobs'].append(jobid)
    resources = get_consumed_resources(jobid, runtime=job_runtime, job_data=data)
    remaining_cpu_hours = ret['remaining_quota']['cpu_hours'] - resources['cpu_hours']
    remaining_mem_hours = ret['remaining_quota']['memory_hours'] - resources['memory_hours']
    userinfo_col.replace_one(
                {'id': userid},
                {
                    'id': userid,
                    'jobs': ret['jobs'],
                    'remaining_quota':  {'cpu_hours': remaining_cpu_hours, 'memory_hours': remaining_mem_hours},
                    'total_quota': {'cpu_hours': ret['total_quota']['cpu_hours'], 
                                'memory_hours': ret['total_quota']['memory_hours']}
                }
                )

    # print(batch.log())

    

def create_new_job(user_id, **data):
    if available_quota(user_id) == False:
        return {'status': 'Failed', 'message': 'Available resource quota has been consumed'}, 403

    ## Currently done with multiprocessing but if high traffic is expected it should be Celery with RabbitMQ and Redis
    job = Process(target=submit_job, daemon=True, args=(user_id,), kwargs=data)
    job.start()

    response_object = {
            'status': 'Success',
            'message': 'The job has been submitted',
        }
    return response_object, 200


def get_all_jobs(userid):
    db = get_mongo_conn()
    userinfo_col = db['userinfo']
    ret = userinfo_col.find_one({'id': userid})
    if ret == None:
        job_ids = []
    else:
        job_ids = ret['jobs']
        
    response_object = {
            job_ids
        }
    return response_object, 200

def get_logs_by_id(user_id, job_id):

    # Check if the job id belongs to a user
    db = get_mongo_conn()
    userinfo_col = db['userinfo']
    ret = userinfo_col.find_one({'id': user_id})
    jobs = ret['jobs']
    if job_id not in jobs:
        return {'filename': None}, 404

    # If the job belongs to the user
    target_path =  user_id + '-logs.zip'
    # print(history_server_url + "/api/v1/applications/"+job_id+"/logs")
    response = requests.get(history_server_url + "/api/v1/applications/"+job_id+"/logs", verify=False, stream=True)
    if response.status_code == 404:
        return {'filename': None}, 404

    handle = open('logs/' + target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()

    response_object = {
            'filename': target_path
        }
    return response_object, 200


def get_results_by_id(user_id, job_id):
    response_object = {
            'message': 'This is just a stub atm'
        }

    return response_object, 200
