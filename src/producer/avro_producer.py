import json
import requests
from functools import cached_property
from colorama import Fore, Back, Style, init, deinit

class AvroProducer:
    
    def __init__(self, sensor, headers= {'Content-Type': 'application/vnd.kafka.avro.v2+json'}):
        self.sensor = sensor
        self.headers = headers
    
    @cached_property
    def url(self):
        """URL endpoint to where the message will be posted."""
        return f"{self.sensor.config['DEFAULT']['REST_PROXY']}/topics/{self.sensor.config['PRODUCER']['TOPIC_AVRO']}"
        
    def produce(self):
        """Produce AVRO messages from a DHT11 object.

        Args:
            dht11 (DHT11): DHT11 object
        """
        payload = self.sensor.get_avro_payload()
        res = requests.post(self.url, data=json.dumps(payload), headers=self.headers)
        start = Back.BLUE + Fore.WHITE + '%%% ----- MESSAGE ----- %%%' + Style.RESET_ALL
        end = Back.BLUE + Fore.WHITE + '%%% --- END MESSAGE --- %%%'+ Style.RESET_ALL
        init()
        print(
            f"""
            {start}
            URL:
                {self.url}
            
            Headers:
                {self.headers}
            
            Payload:
                {payload}
                
            Return: 
                {res.text}
            {end}
            
            """.rjust(40,'-')
            )
        deinit()
        