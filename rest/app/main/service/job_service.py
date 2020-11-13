import uuid
import datetime
from multiprocessing import Process, Queue
from livy import LivyBatch
from pymongo import MongoClient
import requests
import json
from ..util.helpers import get_consumed_resources

from app.main import db

# TODO: This needs to be configurable
# LIVY_URL = "http://localhost:8998"
LIVY_URL = "http://livy.se-caid.org"
history_server_url = "https://history.se-caid.org"

config = json.load(open("config.json"))
mongo_host_ip = config["mongo_ip"]
mongo_host_port = config["mongo_port"]
username = config["mongo_username"]
password = config["mongo_password"]
database = config["database"]
client = MongoClient(host=mongo_host_ip, port=mongo_host_port,
                    username = username,
                    password = password,
                    authSource=database
                    )
db = client[database]

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
        idQ.put(jobid)

    except:
        print("An exception has occurred. Terminating the call")
        # return -1 
        jobid = "1"

    
    r = requests.get(history_server_url + "/api/v1/applications/"+jobid, verify=False)
    job_json_data = r.json()
    ## What if jobs in the application fails
    job_runtime = job_json_data["attempts"][0]["duration"]/1000.0

    userinfo_col = db['userinfo']
    ret = userinfo_col.find_one({'id': userid})
    if ret == None:
        # Change the defaults here and pull them from a config file instead
        userinfo_col.insert_one({
                        'id': userid,
                        'jobs': [jobid],
                        'remaining_quota':  {'cpu_hours': 100, 'memory_hours': 100},
                        'total_quota': {'cpu_hours': 100, 'memory_hours': 100}
                        })
    else:
        jobs = ret['jobs'].append(jobid)
        resources = get_consumed_resources(jobid, runtime=job_runtime, job_data=data)
        remaining_cpu_hours = ret['remaining_quota']['cpu_hours'] - resources['cpu_hours']
        remaining_mem_hours = ret['remaining_quota']['memory_hours'] - resources['memory_hours']
        userinfo_col.replace_one(
                    {'id': userid},
                    {
                        'id': userid,
                        'jobs': jobs,
                        'remaining_quota':  {'cpu_hours': remaining_cpu_hours, 'memory_hours': remaining_mem_hours},
                        'total_quota': {'cpu_hours': 100, 'memory_hours': 100}
                    }
                    )

    # print(batch.log())

    

def create_new_job(userid, **data):
    ## Currently done with multiprocessing but if high traffic is expected it should be Celery with RabbitMQ and Redis
    job = Process(target=submit_job, daemon=True, args=(userid), kwargs=data)
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
