# import requests
# import json 

# LIVY_HOST = 'http://livy.se-caid.org'

# directive = '/sessions'
# headers = {'Content-Type': 'application/json'}

# data = {'kind':'pyspark','name':'first-livy'}

# resp = requests.post(LIVY_HOST+directive, headers=headers, data=json.dumps(data), verify=False)

# print(requests.codes.created)
# print(resp.status_code)
# if resp.status_code == requests.codes.created:
#     session_id = resp.json()['id']
# else:
#     print("Error")

# print(session_id)

from livy import LivyBatch

LIVY_URL = "http://livy.se-caid.org"

batch = LivyBatch.create(
    LIVY_URL,
    file=(
        "https://repo.typesafe.com/typesafe/maven-releases/org/"
        "apache/spark/spark-examples_2.11/1.6.0-typesafe-001/"
        "spark-examples_2.11-1.6.0-typesafe-001.jar"
    ),
    class_name="org.apache.spark.examples.SparkPi",
    verify=False,
    spark_conf= {
                "spark.kubernetes.namespace": "spark-cluster",
                "spark.kubernetes.driver.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.mount.path": "/data",
                "spark.kubernetes.driver.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.mount.readOnly": False,
                "spark.kubernetes.driver.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.options.claimName":"events-dir",
                "spark.kubernetes.executor.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.mount.path": "/data",
                "spark.kubernetes.executor.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.mount.readOnly": False,
                "spark.kubernetes.executor.volumes.persistentVolumeClaim.pvc-ddc9eeec-db5f-4134-bb01-becd180ac671.options.claimName":"events-dir"
            },
)
# batch.wait()