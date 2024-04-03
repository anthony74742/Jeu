
class CommunicationCallback:
    
    def __init__(self):
        pass
    
    def connectionCallback(self):
        print("Connected")
    
    def disconnectionCallback(self):
        print("Disconected")
    
    def didReceiveCallback(self,value):
        print(f"Received {value}")
    
    
class WirelessManager:
    
    def __init__(self,bleCallback = None,wsCallback = None):
        self.bleCallback = bleCallback
        self.wsCallback = wsCallback
        
        if self.bleCallback != None:
            from ble_simple_peripheral import bluetooth,BLESimplePeripheral
            self.ble = bluetooth.BLE()
            self.blePeripheral = BLESimplePeripheral(self.ble,name=self.bleCallback.bleName)
            self.blePeripheral.on_write(self.bleCallback.didReceiveCallback)
            
        if self.wsCallback != None:
            from ws_server import WSServer
            self.server = WSServer(self.wsCallback.connectionCallback,self.wsCallback.disconnectionCallback,self.wsCallback.didReceiveCallback)
            self.server.start()
    
    def isConnected(self):
        if self.bleCallback != None:
            return self.blePeripheral.is_connected()
        if self.wsCallback != None:
            return self.server.isConnected
    
    def sendDataToBLE(self,data):
        if self.bleCallback != None:
            if self.blePeripheral.is_connected():
                self.blePeripheral.send(data)
                
    def sendDataToWS(self,data):
        if self.wsCallback != None:
            if self.server.isConnected:
                self.server.sendData(data)
    
    def process(self):
        if self.wsCallback != None:
            self.server.process_all()
    
