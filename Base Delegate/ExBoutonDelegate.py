from machine import Pin
import time

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
        

class Button:
    def __init__(self, pin_number):
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

# Configuration du bouton sur la broche 14
button = Button(33)

# Boucle principale pour tester le bouton
while True:
    button.process()
    time.sleep(0.1)  # Pause pour éviter une boucle trop rapide
