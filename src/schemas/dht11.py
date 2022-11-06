class DHT11Measurement(object):
    """Measurements record from a DHT11 sensor

    Args:
        sensor_id: sensor identifier (str).
        umidity: umidity measurement (float).
        temperature: temperature measurement (float).
        time_8601: datetime in ISO-8601 (str).
        timestamp: datetime in ms since 1/1/1970 (float).
    """
    
    def __init__(self, sensor_id, umidity, temperature, time_8601, timestamp):
        self.sensor_id = sensor_id
        self.umidity = umidity
        self.temperature = temperature
        self.time_8601 = time_8601
        self.timestamp = timestamp