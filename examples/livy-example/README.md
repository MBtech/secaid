## Spark-submit and Livy equivalence
![equivalence](images/equivalent.png "Equivalence")

## Dependencies
If your pyspark job needs some python dependencies, you can zip up the python dependencies and attach the zip as pyfiles

Run the following the get the `requirements.txt` for your pyspark project:
```python
python3 -m pip install pipreqs 
pipreqs <path to your project>
```
Build python dependencies into a zip:
```python
pip install -t dependencies -r requirements.txt
cd dependencies
zip -r ../dependencies.zip .
```

## Troubleshooting
Here are the errors that can come up with the right jar dependencies are not includes:

### Error:
`TypeError: 'JavaPackage' object is not callable` near the Avro related commands

Missing Jar: `spark-avro_2.12-3.0.1.jar`

### Error: 
`java.lang.NoClassDefFoundError: org/apache/commons/pool2/PooledObjectFactory`

Missing Jar: `commons-pool2-2.8.0.jar`

### Error:
`java.lang.NoClassDefFoundError: kafka/common/TopicAndPartition`

Missing Jar: `kafka-clients-2.3.0.jar`

### Error: 
`java.lang.NoClassDefFoundError: org/apache/spark/kafka010/KafkaTokenUtil`

Missing Jar: `spark-token-provider-kafka-0-10_2.12-3.0.1.jar`

### Error:
`java.lang.NoClassDefFoundError: Could not initialize class org.apache.spark.sql.kafka010.consumer.KafkaDataConsumer` or `org.apache.spark.sql.kafka010.KafkaSourceRDDPartition`

Missing Jar: `spark-sql-kafka-0-10_2.12-3.0.1.jar`