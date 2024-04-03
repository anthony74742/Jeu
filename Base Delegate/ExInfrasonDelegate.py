import RPi.GPIO as GPIO
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def measure_distance(self):
        # Envoie d'une impulsion de 10µs pour déclencher le capteur
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        # Mesure du temps de retour de l'onde ultrasonore
        pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()

        # Calcul de la distance en cm
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance

class MyInfraSensor:
    def __init__(self):
        self.sensor = HCSR04(trigger_pin=23, echo_pin=24)  # Exemple de broches GPIO sur le Raspberry Pi

    def process(self):
        distance = self.sensor.measure_distance()
        print("Distance mesurée:", distance, "cm")

    def cleanup(self):
        GPIO.cleanup()

# Exemple d'utilisation
if __name__ == "__main__":
    infra_sensor = MyInfraSensor()
    try:
        infra_sensor.process()
    except KeyboardInterrupt:
        print("Arrêt manuel.")
    finally:
        infra_sensor.cleanup()
