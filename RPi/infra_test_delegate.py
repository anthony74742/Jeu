import RPi.GPIO as GPIO
import time
import websocket
import json
from abc import ABC, abstractmethod

class WebsocketDelegate(ABC):
    @abstractmethod
    def send_data(self, data):
        pass
   
    @abstractmethod
    def cleanup(self):
        pass

class WebSocket(WebsocketDelegate):
    def __init__(self, websocket_url):
        self.websocket_url = websocket_url
        self.ws = None

    def send_data(self, data):
        if self.ws is None or not self.ws.connected:
            self.ws = websocket.create_connection(self.websocket_url)
        message = json.dumps(data)
        self.ws.send(message)

    def cleanup(self):
        if self.ws is not None and self.ws.connected:
            self.ws.close()

class DistanceSensorDelegate(ABC):
    @abstractmethod
    def measure_distance(self, data):
        pass
    
class DistanceSensor(DistanceSensorDelegate):
    def __init__(self):
        pass
    
    def measure_distance(self, sensor, GPIO):
        GPIO.output(sensor.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(sensor.trigger_pin, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(sensor.echo_pin) == 0:
            start_time = time.time()

        while GPIO.input(sensor.echo_pin) == 1:
            stop_time = time.time()

        elapsed_time = stop_time - start_time
        distance = (elapsed_time * 34300) / 2
        
        

class MyDistanceSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.delegate = DistanceSensor()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def measure_distance(self, sensor, GPIO):
        self.delegate.measure_distance(sensor, GPIO)

    def send_data_to_delegate(self, distance):
        data = {"action": "Distance", "data": distance}
        self.delegate.send_data(data)

    def cleanup(self):
        self.delegate.cleanup()
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        websocket_delegate = WebSocket(websocket_url="ws://192.168.26.122:80")
        sensor = MyDistanceSensor(trigger_pin=23, echo_pin=24)
        while True:
            dist = sensor.measure_distance()
            print("Distance mesurée: {:.2f} cm".format(dist))
            sensor.send_data_to_delegate(dist)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du programme...")
    finally:
        sensor.cleanup()
