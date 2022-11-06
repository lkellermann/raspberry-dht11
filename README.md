# Raspberry DHT11

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Thanks!](#thanks)


## About <a name = "about"></a>

This is a simple producer application that streams measurements from a DHT11 sensor in a Raspberry Pi device to an Apache Kafka REST Proxy.

## Getting Started <a name = "getting_started"></a>
To run this experiment you will need:

-  A [DHT11](https://learn.adafruit.com/dht) sensor.
-  A Raspberry Pi-like device or any other board that runs Python.
-  [Docker and Docker Compose](https://docs.docker.com/engine/install/) installed to run the Apache Kafka ecosystem

After this you should download this repository into your host and board device. Change the `setup/dht11.cfg` file accordingly to your setup.
```config
[DEFAULT]
SENSOR_ID=DHT11-RPI
GPIO_PIN=<Pin to where your sensor is sending the signal.>
REST_PROXY=http://<your private IP>:8082
[PRODUCER]
TOPIC=RASPBERRY
```
> Note: the `SENSOR_ID` will also be used as partition key to the Kafka topic.

At your host machine, run the following command at root of this repository:
```shell
docker compose up
```

Wait until all images be downloaded and the containers be created. You will be ready to follow the next steps when you run the command: 
```shell
docker container ls
```
and see something like this:
```dotnetcli
CONTAINER ID   IMAGE                                                  COMMAND                   CREATED        STATUS                 PORTS                                                 NAMES
4d28e5bc6850   confluentinc/cp-kafka-rest:6.1.0                       "/etc/confluent/dock…"    5 hours ago    Up 5 hours             0.0.0.0:8082->8082/tcp, :::8082->8082/tcp             rest-proxy
7a9e2feccc9e   confluentinc/cp-kafka-connect-base:6.2.0               "bash -c 'echo \"Inst…"   23 hours ago   Up 5 hours (healthy)   0.0.0.0:8083->8083/tcp, :::8083->8083/tcp, 9092/tcp   kafka-connect
399503732ae3   confluentinc/cp-enterprise-control-center:6.2.0        "bash -c 'echo \"Wait…"   23 hours ago   Up 5 hours             0.0.0.0:9021->9021/tcp, :::9021->9021/tcp             control-center
7bdf9dc538b3   confluentinc/ksqldb-server:0.21.0                      "/usr/bin/docker/run"     23 hours ago   Up 5 hours             0.0.0.0:8088->8088/tcp, :::8088->8088/tcp             ksqldb
8abf9633cad1   confluentinc/cp-schema-registry:6.2.0                  "/etc/confluent/dock…"    23 hours ago   Up 5 hours             0.0.0.0:8081->8081/tcp, :::8081->8081/tcp             schema-registry
769d1929d384   confluentinc/cp-kafka:6.2.0                            "/etc/confluent/dock…"    23 hours ago   Up 5 hours             0.0.0.0:9092->9092/tcp, :::9092->9092/tcp             broker
9e7abc79f0d4   docker.elastic.co/kibana/kibana:7.10.1                 "/usr/local/bin/dumb…"    23 hours ago   Up 5 hours             0.0.0.0:5601->5601/tcp, :::5601->5601/tcp             kibana
128fb19e6dfc   confluentinc/cp-zookeeper:6.2.0                        "/etc/confluent/dock…"    23 hours ago   Up 5 hours             2181/tcp, 2888/tcp, 3888/tcp                          zookeeper
9dd6d99fb1de   docker.elastic.co/elasticsearch/elasticsearch:7.10.1   "/tini -- /usr/local…"    23 hours ago   Up 5 hours             0.0.0.0:9200->9200/tcp, :::9200->9200/tcp, 9300/tcp   elasticsearch
95c8751b82ba   edenhill/kafkacat:1.6.0                                "/bin/sh -c 'apk add…"    23 hours ago   Up 5 hours                                                                   kafkacat
```

After that set the working directory in your board device to be the root of this repository and install the `requirements.txt` packages into the Python virtual Environment in your board. Then you should be good to run the producer application with the following command:
```
python src/main.py
```
To interrupt the execution, press `Control+C`.

## Thanks! <a name = "thanks"></a>
Thanks to [@rmoff](https://github.com/rmoff) for providing the docker files and his tutorials at his channel on [youtube](https://www.youtube.com/c/rmoff).