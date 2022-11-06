import RPi.GPIO as GPIO 
from sensors.dht11 import DHT11
from producer.dht11 import producer

GPIO.setmode(GPIO.BOARD)

def main():
    """
    Configure sensor object to execute measurements and send data to producer via REST API proxy.
    """
    dht11 = DHT11('setup/dht11.cfg')
    try:
        while True:
            producer(dht11)
    except KeyboardInterrupt:
        print('End')

if __name__ == '__main__':
    main()
