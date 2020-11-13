import sys
from random import random
from operator import add

from pyspark.sql import SparkSession
from pyspark.sql.functions import split

from pyspark import SparkContext

import avro.schema
import json
import requests
from pyspark.sql.column import Column, _to_java_column 

def from_avro(col, jsonFormatSchema): 
    sc = SparkContext._active_spark_context 
    avro = sc._jvm.org.apache.spark.sql.avro
    f = getattr(getattr(avro, "package$"), "MODULE$").from_avro
    return Column(f(_to_java_column(col), jsonFormatSchema)) 


def to_avro(col): 
    sc = SparkContext._active_spark_context 
    avro = sc._jvm.org.apache.spark.sql.avro
    f = getattr(getattr(avro, "package$"), "MODULE$").to_avro
    return Column(f(_to_java_column(col))) 

if __name__ == "__main__":
    """
        Read data and process data from Kafka as a batch job
    """
    # KAFKA_BROKER="10.43.43.139:9092"
    KAFKA_BROKER="kafka.se-caid.org:9092"

    # SCHEMA_PATH = "traffic.avsc"
    # SCHEMA = open(SCHEMA_PATH).read()
    SCHEMA_PATH = "https://secaid-bucket.s3.eu-west-2.amazonaws.com/traffic.avsc"
    f = requests.get(SCHEMA_PATH)
    SCHEMA = f.text
    print(type(SCHEMA))
    print(SCHEMA)
    
    # SCHEMA_PATH = "secaid-bucket/traffic.avsc"
    # SCHEMA = s3_read(SCHEMA_PATH)

    s = json.loads(SCHEMA)["fields"]
    print(s)

    spark = SparkSession\
        .builder\
        .appName("PySpark-Kafka-1")\
        .getOrCreate()
    
    df = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", "traffic-data") \
        .option("startingOffsets", "earliest")\
        .load()

    df.show(10)

    df_data = df.select(from_avro("value", SCHEMA).alias("Data"))
    length = len(df_data.select('Data').take(1)[0][0])
    df_data = df_data.select([df_data["Data"][s[i]["name"]].alias(s[i]["name"]) for i in range(length)])
    
    df_data.show(10)
    df_data.groupBy('source').sum('nflows').show()