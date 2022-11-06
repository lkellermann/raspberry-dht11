import json
import requests


def get_payload(dht11):
    """Generates payload from DHT11 object.

    Args:
        dht11 (DHT11): object containing sensor measurements and its configurations.

    Returns:
        dict: dictionary representing the payload to be sent to the REST Kafka proxy.
    """
    measurement=dht11.read_sensor()
    payload = {
        "records":
            [
                {
                "key": dht11.config['DEFAULT']['SENSOR_ID'],
                "value":{
                        "sensor_id": measurement.sensor_id,
                        "umidity": measurement.umidity,
                        "temperature": measurement.temperature,
                        "time_8601": measurement.time_8601,
                        "timestamp": measurement.timestamp
                    }
                }
            ]
        }
    return payload


def producer(dht11):
    """_summary_

    Args:
        dht11 (_type_): _description_
    """
    url=f"{dht11.config['DEFAULT']['REST_PROXY']}/topics/{dht11.config['PRODUCER']['TOPIC']}"
    headers={'Content-Type': 'application/vnd.kafka.json.v2+json'}
    payload = get_payload(dht11)
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"""
        %%% ----- MESSAGE ----- %%%
          Payload:
          {payload}
            
          Return: 
            {res.text}
            
        %%% --- END MESSAGE --- %%%
          """
        )
    