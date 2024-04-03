from time import sleep_ms 
import bluetooth
import random
import struct
import time
from wireless_manager import *
from machine import Pin
import json

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

                
            
wirelessManager = WirelessManager(BLECallback("Antho"),WebsocketCallback())        

def send_value(value):
    wirelessManager.sendDataToWS(value)

morse_code = {
    'A': '01',
    'B': '1000',
    'C': '1010',
    'D': '100',
    'E': '0',
    'F': '0010',
    'G': '110',
    'H': '0000',
    'I': '00',
    'J': '0111',
    'K': '101',
    'L': '0100',
    'M': '11',
    'N': '10',
    'O': '111',
    'P': '0110',
    'Q': '1101',
    'R': '010',
    'S': '000',
    'T': '1',
    'U': '001',
    'V': '0001',
    'W': '011',
    'X': '1001',
    'Y': '1011',
    'Z': '1100',
    '0': '11111',
    '1': '01111',
    '2': '00111',
    '3': '00011',
    '4': '00001',
    '5': '00000',
    '6': '10000',
    '7': '11000',
    '8': '11100',
    '9': '11110',
    '.': '010101',
    ',': '110011',
    '?': '001100',
    '\'': '011110',
    '!': '101011',
    '/': '10010',
    '(': '10110',
    ')': '101101',
    '&': '01000',
    ':': '111000',
    ';': '101010',
    '=': '10001',
    '+': '01010',
    '-': '100001',
    '_': '001101',
    '"': '010010',
    '$': '0001001',
    '@': '011010',
    ' ': ' '
}

class MorseTranslator:
    def __init__(self) -> None:
        self.btnIsPressed = False
        self.btnStartTime = 0
        self.btnEndTime = 0
        self.shortPressDelta = 300  # Delta pour un appui court (en millisecondes)
        self.morseWord = ""
        self.lastClickTime = 0
        self.tabWord = ""
        self.isSend = False

    def onChangeButton(self, pin):
        if pin.value() == 1:  # Si le bouton est enfoncé
            self.btnStartTime = time.ticks_ms()
            self.btnIsPressed = True
            self.lastClickTime = self.btnStartTime  # Initialiser lastClickTime lorsque le bouton est enfoncé
        else:  # Si le bouton est relâché
            if self.btnIsPressed:  # Vérifie si le bouton était déjà pressé
                self.btnEndTime = time.ticks_ms()
                self.btnIsPressed = False
                self.processPressDuration()

    def processPressDuration(self):
        pressDuration = self.btnEndTime - self.btnStartTime
        if pressDuration < self.shortPressDelta:
            print("Appui court détecté")
            self.morseWord += "0"  # Ajoute un point (click court) à la séquence Morse
        else:
            print("Appui long détecté")
            self.morseWord += "1"  # Ajoute un trait (click long) à la séquence Morse
        print(self.morseWord)
        self.lastClickTime = time.ticks_ms()  # Met à jour lastClickTime à la fin de chaque appui
        # self.translateMorseWord() # Remarque: vous pouvez appeler cela ici si nécessaire

    def translateMorseWord(self):
        self.morseWord = self.morseWord.strip()  # Retire les espaces de début et de fin
        translated_word = ""
        # Sépare la séquence Morse en mots
        morse_words = self.morseWord.split(" ")
        for morse_word in morse_words:
            # Trouve la lettre correspondante à la séquence Morse dans le dictionnaire
            for letter, code in morse_code.items():
                if morse_word == code:
                    translated_word += letter
                    break
        print("Mot en Morse:", self.morseWord)
        print("Mot traduit:", translated_word)
        self.tabWord += translated_word
        print(self.tabWord)

class Button:
    def __init__(self, pin, morse_translator) -> None:
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=morse_translator.onChangeButton)
        self.lastTranslateTime = 0 

    def process(self):
        current_time = time.ticks_ms()
        if not morse_translator.btnIsPressed and current_time - morse_translator.lastClickTime > morse_translator.shortPressDelta:
            # Si aucun appui n'est en cours et qu'aucun clic n'a été détecté dans les 300 ms précédents
            if morse_translator.morseWord:
                morse_translator.translateMorseWord()
                morse_translator.morseWord = ""
                morse_translator.isSend = False
                
            if current_time - morse_translator.lastClickTime > 3 * morse_translator.shortPressDelta and not morse_translator.isSend:
                morse_translator.isSend = True
                # Si le temps écoulé depuis le dernier clic est inférieur à 900 ms
                # Si le temps écoulé depuis le dernier clic est supérieur à 900 ms
                if len(morse_translator.tabWord) != 0:
                    print("Send !!!!!")
                    Json = {'action': 'Text', 'data': morse_translator.tabWord}
                    Json = json.dumps(Json)
                    wirelessManager.sendDataToWS(Json)
                    morse_translator.tabWord = ""
                    self.lastTranslateTime = current_time  # Mettre à jour le temps du dernier clic

# Initialisation
morse_translator = MorseTranslator()
try:
    button = Button(33, morse_translator)
    while True:
        wirelessManager.process()
        time.sleep_ms(50)
        button.process()
except KeyboardInterrupt:
    pass