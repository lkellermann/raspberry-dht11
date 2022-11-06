import configparser
import functools
import Adafruit_DHT
from datetime import datetime
from schemas.dht11 import DHT11Measurement
class DHT11:

    def __init__(self, config):
        self._config = config
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
                         timestamp = now.timestamp()
                         )
