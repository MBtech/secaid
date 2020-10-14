import sys
from random import random
from operator import add

from pyspark.sql import SparkSession
from pyspark.sql.functions import split

from pyspark import SparkContext

import avro.schema
import json
import boto3
import requests
from pyspark.sql.column import Column, _to_java_column 

def s3_read(source, profile_name=None):
    """
    Read a file from an S3 source.

    Parameters
    ----------
    source : str
        Path starting without s3://, e.g. 'bucket-name/key/foo.bar'
    profile_name : str, optional
        AWS profile

    Returns
    -------
    content : str

    botocore.exceptions.NoCredentialsError
        Botocore is not able to find your credentials. Either specify
        profile_name or add the environment variables AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN.
        See https://boto3.readthedocs.io/en/latest/guide/configuration.html
    """
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')
    bucket_name, key = source.split('/', 1)
    s3_object = s3.get_object(Bucket=bucket_name, Key=key)
    body = s3_object['Body']
    return body.read().decode("utf-8") 

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
        .appName("PySpark-Kafka")\
        .getOrCreate()
    
    df = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka.se-caid.org:9092") \
        .option("subscribe", "traffic-data") \
        .option("startingOffsets", "earliest")\
        .load()

    df.show(10)

    df_data = df.select(from_avro("value", SCHEMA).alias("Data"))
    length = len(df_data.select('Data').take(1)[0][0])
    df_data = df_data.select([df_data["Data"][s[i]["name"]].alias(s[i]["name"]) for i in range(length)])
    
    df_data.show(10)
    df_data.groupBy('source').sum('nflows').show()