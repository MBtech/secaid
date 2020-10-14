import io
import avro.schema
import avro.io
from kafka import KafkaConsumer
from kafka.structs import TopicPartition

brokers = ['kafka.se-caid.org:9092']

# To consume messages
CONSUMER = KafkaConsumer("traffic-data",
                         group_id='my-group',
                        auto_offset_reset = 'earliest',
                         bootstrap_servers=brokers)

SCHEMA_PATH = "traffic.avsc"
SCHEMA = avro.schema.parse(open(SCHEMA_PATH).read())

for msg in CONSUMER:
    bytes_reader = io.BytesIO(msg.value)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(SCHEMA)
    traffic_data = reader.read(decoder)
    print(traffic_data)
