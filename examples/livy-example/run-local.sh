~/Downloads/spark-3.0.1-bin-hadoop2.7/bin/spark-submit \
--jars https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.0.1/spark-sql-kafka-0-10_2.12-3.0.1.jar,\
https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.3.0/kafka-clients-2.3.0.jar,\
https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.0.1/spark-token-provider-kafka-0-10_2.12-3.0.1.jar,\
https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.8.0/commons-pool2-2.8.0.jar,\
https://repo1.maven.org/maven2/org/apache/spark/spark-avro_2.12/3.0.1/spark-avro_2.12-3.0.1.jar \
pyspark_kafka.py