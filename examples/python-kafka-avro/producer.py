import io
import random
import avro.schema
from avro.io import DatumWriter
from kafka import KafkaProducer
from kafka import KafkaClient
from kafka.admin import KafkaAdminClient, NewTopic
import pandas as pd

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
topic_name = "traffic-data"

client = KafkaClient(bootstrap_servers=['localhost:9092'])
future = client.cluster.request_update()
client.poll(future=future)
metadata = client.cluster
print(metadata.topics())
if topic_name not in metadata.topics():
    admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'])

    topic_list = []
    topic_list.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)


# Path to user.avsc avro schema
schema_path = "traffic.avsc"
schema = avro.schema.parse(open(schema_path).read())

data = pd.read_csv('traffic_data.csv')
# print(data)
print(producer.bootstrap_connected())

for index, row in data.iterrows():
    # print(row)
    writer = DatumWriter(schema)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write({"date": row["date"], "source": row["l_ipn"], "target": row["r_asn"],
                             "nflows": row["f"]}, encoder)
    raw_bytes = bytes_writer.getvalue()
    # print(raw_bytes)
    future = producer.send(topic_name, raw_bytes)

producer.flush()
# result = future.get(timeout=300)