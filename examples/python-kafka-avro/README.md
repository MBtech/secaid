This is a simple example to create a producer (producer.py) and a consumer (consumer.py) to demo production and consumption of Kafka messages serialized using Avro

## Setup
- Install packets via PIP: `pip install -r requirements.txt`
- Setup a port-forward to the se-caid cluster's kafka broker:
    ```kubectl --insecure-skip-tls-verify -n kafka port-forward service/kafka-cp-kafka 9092:9092```
## Usage
Run producer:
```
python producer.py
```

Run consumer:
```
python  consumer.py
```


