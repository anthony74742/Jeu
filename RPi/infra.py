import RPi.GPIO as GPIO
import time
import websocket
import json


class DistanceSensor:
    def __init__(self, trigger_pin, echo_pin, delegate):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.delegate = delegate
        self.websocket_url = "ws://192.168.26.122:80"
        self.ws = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def measure_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        elapsed_time = stop_time - start_time
        distance = (elapsed_time * 34300) / 2

        return distance

    def send_data_to_websocket(self, distance):
        if self.delegate is not None:
            self.delegate.send_data(distance)

    def cleanup(self):
        if self.ws is not None and self.ws.connected:
            self.ws.close()
        GPIO.cleanup()

class Delegate:
    def __init__(self):
        self.websocket_url = "ws://192.168.26.122:80"
        self.ws = None

    def send_data(self, distance):
        data = {"action": "Distance", "data": distance}
        message = json.dumps(data)
        if self.ws is None or not self.ws.connected:
            self.ws = websocket.create_connection(self.websocket_url)
        self.ws.send(message)

if __name__ == '__main__':
    try:
        delegate = Delegate()
        sensor = DistanceSensor(trigger_pin=23, echo_pin=24, delegate=delegate)
        while True:
            dist = sensor.measure_distance()
            print("Distance mesurée: {:.2f} cm".format(dist))
            sensor.send_data_to_websocket(dist)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du programme...")
    finally:
        sensor.cleanup()