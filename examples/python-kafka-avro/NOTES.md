# Troubleshooting
Make sure that kafka broker is accessible. Use `kafkacat` (`brew install kafkacat`)

`kafkacat -L -b kafka.se-caid.org:9092`

Consume data

`kafkacat -b kafka.se-caid.org:9092 -C -t traffic-data`

## If you need to port forward the broker
- Setup a port-forward to the k8s cluster's kafka broker:
    ```kubectl --insecure-skip-tls-verify -n kafka port-forward service/kafka-cp-kafka 9092:9092```

