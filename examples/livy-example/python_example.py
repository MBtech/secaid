from livy import LivyBatch

LIVY_URL = "http://livy.se-caid.org"

batch = LivyBatch.create(
    LIVY_URL,
    file=(
        "s3://pyspark_kafka.py"
    ),
    verify=False,
    spark_conf= {
                "spark.jars.packages": ['org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1'],
                "spark.kubernetes.namespace": "livy"
            },
)