import io
import random
import avro.schema
from avro.io import DatumWriter
from kafka import KafkaProducer
from kafka import KafkaClient

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
topic_name = "topic"

# Path to user.avsc avro schema
schema_path = "user.avsc"
schema = avro.schema.parse(open(schema_path).read())

for i in range(10):
    writer = DatumWriter(schema)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write({"name": "123", "favorite_color": "111", "favorite_number": random.randint(0, 10)}, encoder)
    raw_bytes = bytes_writer.getvalue()
    # print(raw_bytes)
    future = producer.send(topic_name, raw_bytes)
    result = future.get(timeout=60)