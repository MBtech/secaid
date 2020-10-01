import sys
from random import random
from operator import add

from pyspark.sql import SparkSession

import avro.schema

if __name__ == "__main__":
    """
        Read data and process data from Kafka as a batch job
    """
    spark = SparkSession\
        .builder\
        .appName("PySpark-Kafka")\
        .getOrCreate()
    
    df = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka.se-caid.org:9092") \
        .option("subscribe", "traffic-data") \
        .load()

    df.show(10)