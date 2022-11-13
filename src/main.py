import RPi.GPIO as GPIO 
from sensors.dht11 import DHT11
from producer.avro_producer import AvroProducer
from producer.json_producer import JsonProducer

GPIO.setmode(GPIO.BOARD)

def main():
    """
    Configure sensor object to execute measurements and send data to producer via REST API proxy.
    """
    dht11 = DHT11('setup/dht11.cfg')
    dht_avro = AvroProducer(dht11)
    dht_json = JsonProducer(dht11)
    try:
        while True:
            dht_avro.produce()
            dht_json.produce()
    except KeyboardInterrupt:
        print('End')

if __name__ == '__main__':
    main()
