from livy import LivyBatch

LIVY_URL = "http://livy.se-caid.org"

batch = LivyBatch.create(
    LIVY_URL,
    py_files=[
         "https://secaid-bucket.s3.eu-west-2.amazonaws.com/dependencies.zip"
    ],
    file=(
        "https://secaid-bucket.s3.eu-west-2.amazonaws.com/pyspark_kafka.py"
    ),
    jars=["https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.0.1/spark-sql-kafka-0-10_2.12-3.0.1.jar",
    "https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.3.0/kafka-clients-2.3.0.jar",
    "https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.8.0/commons-pool2-2.8.0.jar",
    "https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.0.1/spark-token-provider-kafka-0-10_2.12-3.0.1.jar",
    "https://repo1.maven.org/maven2/org/apache/spark/spark-avro_2.12/3.0.1/spark-avro_2.12-3.0.1.jar",
    ],
    verify=False,
    spark_conf= {
                "spark.kubernetes.namespace": "livy"
            },
)
    #  "spark.jars": "spark-sql-kafka-0-10_2.12:3.0.1.jar,spark-avro_2.12:3.0.1.jar",
                # "spark.jars.packages": "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,\
                #     org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.0.1,\
                #         org.apache.spark:spark-avro_2.12:3.0.1",