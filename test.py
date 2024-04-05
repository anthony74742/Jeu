from time import sleep_ms 
import bluetooth
import random
import struct
import time
from wireless_manager import *
from machine import Pin
import json
import network


class BLECallback(CommunicationCallback):

    def __init__(self,bleName="Default"):
        self.bleName = bleName
    
    def connectionCallback(self):
        print("Connected")
    
    def disconnectionCallback(self):
        print("Disconected")
    
    def didReceiveCallback(self,value):
        print(f"Received {value}")
    
class WebsocketCallback(CommunicationCallback):

    def __init__(self):
        pass
    
    def connectionCallback(self):
        print("Connected")
    
    def disconnectionCallback(self):
        print("Disconected")
    
    def didReceiveCallback(self,value):
        print(f"Received {value}")
        
        def compter_occurrences(caractere, chaine):
            count = 0
            for char in chaine:
                if char == caractere:
                    count += 1
            return count
        
        if compter_occurrences("{", value) <= 1 :
            Json = json.loads(value)
            if Json["action"] :
                print("Action defined")
                if Json["action"] == "Distance" :
                    send_value(value)

                




'''
Setup
'''

class TestableInterface:
    def __init__(self):
        pass

    def test(self):
        raise NotImplementedError("Subclasses must implement test method.")


class SetupESP32:
    def __init__(self, devices, display):
        self.devices = devices
        self.display = display

    def test(self):
        print("Testing ESP32 setup...")
        for device in self.devices:
            result = device.test()
            if result:
                self.display.confirm_test(device.__class__.__name__)
            else:
                self.display.reject_test(device.__class__.__name__)
            time.sleep(1)


class Network(TestableInterface):
    def __init__(self):
        super().__init__()
        print("Initializing network...")

    def test(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if wlan.isconnected():
            print("Connected to WiFi network.")
            return True
        else:
            print("Failed to connect to WiFi network.")
            return False

class Websocket(TestableInterface):
    def __init__(self):
        super().__init__()
        print("Initializing websocket...")

    def test(self):
        print("Checking websocket server launch... Connected")
        return True


'''
Button
'''

class InterfaceButtonDelegate:
    def button_pressed(self):
        pass
    
    def button_released(self):
        pass
    

class ButtonDelegate(InterfaceButtonDelegate):
    def button_pressed(self):
        print("Action déléguée lors de l'appui sur le bouton")
        Json = {'action': 'Text', 'data': 1}
        Json = json.dumps(Json)
        wirelessManager.sendDataToWS(Json)
    
    def button_released(self):
        print("Action déléguée lors du relachement du bouton")
        Json = {'action': 'Text', 'data': 0}
        Json = json.dumps(Json)
        wirelessManager.sendDataToWS(Json)
        

class Button(TestableInterface):
    def __init__(self, pin_number):
        super().__init__()
        print("Initializing button...")
        self.pin = Pin(pin_number, Pin.IN)
        self.last_state = self.pin.value()
        self.delegate = ButtonDelegate()

    def process(self):
        current_state = self.pin.value()
        if current_state != self.last_state:
            if current_state == 1:  # Bouton relâché
                self.delegate.button_pressed()
            else:
                self.delegate.button_released()
            self.last_state = current_state
    
    def test(self):
        isPushed = False
        timer = time.ticks_ms()
        print("Wait to click !!!!")
        while not isPushed:
            current_state = self.pin.value()
            if current_state == 1:
                isPushed = True
                
            if timer > 10000:
                return False
            
            time.sleep(0.05)
        return True

class Display:
    def __init__(self):
        pass

    def confirm_test(self, test_name):
        print(f"{test_name} test passed.")

    def reject_test(self, test_name):
        print(f"{test_name} test failed.")

led = Pin(2, Pin.OUT)
"""
#Initialisation des objets
button = Button(33)            
wirelessManager = WirelessManager(BLECallback("Antho"),WebsocketCallback())
networks = Network()

# Utilisation
devices = [networks, wirelessManager, button]
display = Display()
setup = SetupESP32(devices, display)
setup.test()
"""
while True:
    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)
# Boucle principale pour tester le bouton
while True:
    button.process()
    time.sleep(0.1)  # Pause pour éviter une boucle trop rapide

