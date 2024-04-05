import Foundation

enum ErrorCode {
    case A,B,C
}

protocol Identifiable {
    var id:UUID { get }
}

protocol SensorDelegate:Identifiable {
    func action()
}

class SensorBrain:SensorDelegate {
    
    var id = UUID()
    
    func action() {
        
    }
    
}

class Sensor1 {
    
    var delegate:SensorDelegate?
    
    func process() {
        // -----
        
        delegate?.action()
    }
}

class TimeManager {
    
    var lastTime = Date()
    var wholeProcessTime = 4.0
    var margin = 1.2
    var timer:Timer?
    
    func feed(){
        lastTime = Date()
        timer?.invalidate()
        timer = Timer.scheduledTimer(withTimeInterval: wholeProcessTime*margin, repeats: false, block: timerCallback)
    }
   
    func timerCallback(t1:Timer) {
        print("RED ALERT!")
    }
    
}

class Watchdog {
    static let instance = Watchdog()
    var canRun = true
    var logs = [String]()
    var timeManagers : [UUID:TimeManager] = [:]
    
    func getLogArray() -> [String] {
        return logs
    }
    
    func getLogStr() -> String {
        return logs.joined(separator: "\n")
    }
    
}


//  T0-----TN  OK
//  T0--------TN OK
//  T0----------------------------------TN NOK


var sensor1 = Sensor1()

//while(true){
    // T0
    if Watchdog.instance.canRun {
        sensor1.process()
        // Truc avec capteur 2
        // Truc avec capteur 3
        // TN
    }else{
        
        // ça va pas
        print(Watchdog.instance.getLogStr())
        
    }
//}