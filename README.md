# Raspberry DHT11

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Elasticsearch integration](#elastic)
- [Dashboard on Kibana](#kibana)
- [Thanks!](#thanks)



## About <a name = "about"></a>

This is a simple producer application that streams measurements from a DHT11 sensor in a Raspberry Pi device to an Apache Kafka REST Proxy.

https://user-images.githubusercontent.com/9287209/200188360-1a7e4e0f-3a5d-4e68-af99-471aa2f32ab9.mp4

## Getting Started <a name = "getting_started"></a>
To run this experiment you will need:

-  A [DHT11](https://learn.adafruit.com/dht) sensor.
-  A Raspberry Pi-like device or any other board that runs Python.
-  [Docker and Docker Compose](https://docs.docker.com/engine/install/) installed to run the Apache Kafka ecosystem

After this you should download this repository into your host and board device. Change the `setup/dht11.cfg` file accordingly to your setup.
```config
[DEFAULT]
SENSOR_ID=DHT11-RPI
GPIO_PIN=4
REST_PROXY=http://192.168.0.7:8082
AVRO_VALUE_SCHEMA=src/avro/dht11.avsc
[PRODUCER]
TOPIC_JSON=json-raspberry
TOPIC_AVRO=avro-raspberry
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

## Elasticsearch Integration <a name = "elastic"></a>
You can send the measurements to Elasticsearch and develop a dashboard on Kibana by executing the following steps:

### 1 - Create an index on Elasticsearch:
- Access Kibana on your browser at `localhost:5601`
- On the side menu, go to `Management` and `Dev Tools`. Create an index by executing the following command:
    ```
    put /avro-raspberry
    {
    "settings":{
        "number_of_shards":1,
        "number_of_replicas":1
    },
    "mappings":{
        "properties":{
        "sensor_id":{"type":"text"},
        "umidity":{"type":"double"},
        "temperature": {"type": "double"},
        "time_8601": {"type": "text"},
        "timestamp":{"type": "date",
            "format": "strict_date_optional_time||epoch_second"
        }
        }
    }
    }
    ```
  - You should receive the following response:

    ```
    {
    "acknowledged" : true,
    "shards_acknowledged" : true,
    "index" : "avro-raspberry"
    }

    ```
### 2 - Create an index pattern on Kibana:
- On the side menu, click on `Management > Stack Management`.
- On the new window, click on `Kibana > Index Patterns`.
- Click on `Create index pattern`.
- Insert the pattern `avro-raspberry*` to select all indexes that begins with `avro-raspberry`. Click on `Next`.
- Under `Time field` select `timestamp`.
- Click on `Create`.

### 3 - Create a connector on Kafka Connector:
- Execute the following command at your terminal:
    ```sh
    curl -i -X PUT -H  "Content-Type:application/json" \
        http://localhost:8083/connectors/sink-raspberry-elastic/config \
        -d '{
            "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
            "topics": "avro-raspberry",
            "connection.url": "http://elasticsearch:9200",
            "type.name": "type.name=kafkaconnect",
            "key.ignore": "true",
            "schema.ignore": "true",
            "errors.log.include.messages": "true",
            "errors.log.enable": "true"
        }'
    ```
  - You should get the following output:
    ```sh
    HTTP/1.1 201 Created
    Date: Mon, 14 Nov 2022 13:09:29 GMT
    Location: http://localhost:8083/connectors/sink-raspberry-elastic
    Content-Type: application/json
    Content-Length: 398
    Server: Jetty(9.4.40.v20210413)

    {"name":"sink-raspberry-elastic","config":{"connector.class":"io.confluent.connect.elasticsearch.ElasticsearchSinkConnector","topics":"avro-raspberry","connection.url":"http://elasticsearch:9200","type.name":"type.name=kafkaconnect","key.ignore":"true","schema.ignore":"true","errors.log.include.messages":"true","errors.log.enable":"true","name":"sink-raspberry-elastic"},"tasks":[],"type":"sink"}
    ```


- Test if the task is being executed by running the following command:
    ```shell
    curl localhost:8083/connectors/sink-raspberry-elastic/tasks | jq
    ```
    - If everything is OK, you will receive the following response:
    ```shell
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100   468  100   468    0     0   144k      0 --:--:-- --:--:-- --:--:--  228k
    [
    {
        "id": {
        "connector": "sink-raspberry-elastic",
        "task": 0
        },
        "config": {
        "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
        "type.name": "type.name=kafkaconnect",
        "errors.log.include.messages": "true",
        "task.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkTask",
        "topics": "avro-raspberry",
        "name": "sink-raspberry-elastic",
        "connection.url": "http://elasticsearch:9200",
        "key.ignore": "true",
        "errors.log.enable": "true",
        "schema.ignore": "true"
        }
    }
    ]
    ```
### 4 - Testing the connection:
- You can test the connection on Kibana console by running the following command:
    ```
    get /avro-raspberry/_search
    ```

- The output will look like the snippet bellow. Note that if your integration is fine the number of total hits will increase:
    ```
    {
    "took" : 0,
    "timed_out" : false,
    "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
    },
    "hits" : {
        "total" : {
        "value" : 869,
        "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
        {
            "_index" : "avro-raspberry",
            "_type" : "_doc",
            "_id" : "avro-raspberry+0+0",
            "_score" : 1.0,
            "_source" : {
            "sensor_id" : "DHT11-RPI",
            "umidity" : 40.0,
            "temperature" : 28.0,
            "time_8601" : "2022-11-13T14:30:15.455864",
            "timestamp" : 1668360615
            }
        },
        {
            "_index" : "avro-raspberry",
            "_type" : "_doc",
            "_id" : "avro-raspberry+0+1",
            "_score" : 1.0,
            "_source" : {
            "sensor_id" : "DHT11-RPI",
            "umidity" : 40.0,
            "temperature" : 28.0,
            "time_8601" : "2022-11-13T14:40:10.704240",
            "timestamp" : 1668361211
            }
    ...
    ```
- You can also test the integration by executing the following command at your terminal:
    ```sh
    curl -s http://localhost:9200/avro-raspberry/_search     -H 'content-type: application/json'     -d '{ "size": 5, "sort": [ { "timestamp": { "order": "desc" } } ] }' |    jq '.hits.hits[]._source | .sensor_id, .umidity,.temperature, .time_8601, .timestamp'
    ```
    - You will get the following response:
    ```sh
    "DHT11-RPI"
    44
    26
    "2022-11-14T10:28:57.957854"
    1668432538
    "DHT11-RPI"
    59
    25
    "2022-11-14T10:28:43.775422"
    1668432524
    "DHT11-RPI"
    60
    25
    "2022-11-14T10:28:34.760165"
    1668432515
    "DHT11-RPI"
    60
    26
    "2022-11-14T10:28:05.459063"
    1668432485
    "DHT11-RPI"
    59
    25
    "2022-11-14T10:27:33.537942"
    1668432454

    ```
## Dashboard on Kibana <a name = "kibana"></a>


## Thanks! <a name = "thanks"></a>
Thanks to [@rmoff](https://github.com/rmoff) for providing the docker files and his tutorials at his channel on [youtube](https://www.youtube.com/c/rmoff).
