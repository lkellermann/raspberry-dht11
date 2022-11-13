import configparser
import functools
import json
from datetime import datetime
import Adafruit_DHT
from helper.my_decorators import singleton

from schemas.dht11 import DHT11Measurement

@singleton
class DHT11:
    """Defines an DHT11 sensor object."""

    def __init__(self, config):
        self._config = config
        self._avro_schema = self.avro_schema
        self.sensor = Adafruit_DHT.DHT11

    @functools.cached_property
    def config(self):
        """Getter method to parse configuration file.

        Returns:
            configparser object with producer configurations.
        """
        con = configparser.ConfigParser()
        con.read(self._config)
        return con
    
    @functools.cached_property
    def avro_schema(self):
        """_summary_

        Args:
            dht11 (_type_): _description_

        Returns:
            _type_: _description_
        """
        with open(self.config['DEFAULT']['AVRO_VALUE_SCHEMA'], 'r', encoding='utf8') as f:
            data_value = json.load(f)
        return data_value

    def read_sensor(self):
        """Method to get sensor measurements.

        Returns:
            DHT11Measurement object containing sensor measurements.
        """
        umid, temp = Adafruit_DHT.read_retry(self.sensor, self.config['DEFAULT']['GPIO_PIN'])
        now = datetime.now()
        return DHT11Measurement(sensor_id = self.config['DEFAULT']['SENSOR_ID'],
                         umidity = umid,
                         temperature = temp,
                         time_8601 = now.isoformat(),
                         timestamp = round(now.timestamp())
                         )
        
    def get_avro_payload(self):
        """Generates AVRO payload.

        Returns:
            dict: dictionary representing the payload to be sent to the REST Kafka Proxy.
        """
        measurement=self.read_sensor()
        payload = {
            "value_schema": json.dumps(self.avro_schema),
            "records":
                [
                    {
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
    
    def get_json_payload(self):
        """Generates JSON payload.

        Returns:
            dict: dictionary representing the JSON payload to be sent to the REST Kafka proxy.
        """
        measurement=self.read_sensor()
        payload = {
            "records":
                [
                    {
                    "key": self.config['DEFAULT']['SENSOR_ID'],
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
