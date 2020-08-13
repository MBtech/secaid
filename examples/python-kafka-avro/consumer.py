import io
import avro.schema
import avro.io
from kafka import KafkaConsumer

# To consume messages
CONSUMER = KafkaConsumer('traffic-data',
                         group_id='my_group',
                         bootstrap_servers=['localhost:9092'])

SCHEMA_PATH = "traffic.avsc"
SCHEMA = avro.schema.parse(open(SCHEMA_PATH).read())

for msg in CONSUMER:
    bytes_reader = io.BytesIO(msg.value)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(SCHEMA)
    traffic_data = reader.read(decoder)
    print(traffic_data)
