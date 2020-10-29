import logging
import socket
import threading
import time
import onionGpio
from temperatureSensor import TemperatureSensor
import oneWire

gpioMode = False
gpioNum = 1 # set the relay GPIO
gpioObj = None

sensor = None
oneWireGpio = 0 # set the sensor GPIO
relayAddr = 7
relayMode = True

try:
    from OmegaExpansion import relayExp
except ImportError:
    relayMode = False
    gpioMode = True

HOST = ''
PORT = 50005

criticalTemp = 30.0
autoSwitch = True
interval = 5

def monitor(name):
    while True:
        if autoSwitch == True:
            # check the temperature value
            temp = sensor.readValue()
            logging.info("Temperature: %s", temp)
            
            # Relay Expansion
            if relayMode == True:
                relayStatus = relayExp.readChannel(relayAddr, 0)
                
                if (temp >= criticalTemp and relayStatus == 0):
                    relayExp.setChannel(relayAddr, 0, 1)
                    logging.info("Enable the electrical circuit by Relay Expansion")
                
                elif (temp < criticalTemp and relayStatus == 1):
                    relayExp.setChannel(relayAddr, 0, 0)
                    logging.info("Disable the electrical circuit by Relay Expansion")
            
            # GPIO, if Relay Expansion not available
            if gpioMode == True:
                gpioStatus = int(gpioObj.getValue())

                if (temp >= criticalTemp and gpioStatus == 0):
                    gpioObj.setValue(1)
                    logging.info("Enable the electrical circuit by GPIO")
                
                elif (temp < criticalTemp and gpioStatus == 1):
                    gpioObj.setValue(0)
                    logging.info("Disable the electrical circuit by GPIO")
            
        time.sleep(interval)

def __main__():
    global sensor, autoSwitch, relayMode, gpioMode, gpioObj
    
    # Temperature sensor configuration
    if not oneWire.setupOneWire(str(oneWireGpio)):
        print("Kernel module could not be inserted. Please reboot and try again.")
        return -1
    
    sensorAddress = oneWire.scanOneAddress()
    
    sensor = TemperatureSensor("oneWire", { "address": sensorAddress, "gpio": oneWireGpio })
    if not sensor.ready:
        print("Sensor was not set up correctly. Please make sure that your sensor is firmly connected to the GPIO specified above and try again.")
        return -1

    # check if Relay Expansion is available
    if relayMode == True:
        try:
            relayExp.driverInit(relayAddr)
            if (relayExp.checkInit(relayAddr) == 0):
                print("The Relay Expansion needs to be initialized")
                relayMode = False
                gpioMode = True
        except:
            relayMode = False
            gpioMode = True
    
    # Enable GPIO mode    
    if gpioMode == True:
        gpioObj = onionGpio.OnionGpio(gpioNum)
        gpioObj.setOutputDirection(0)
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    # Threads that support socket connections
    x = threading.Thread(target = monitor, args=(1,), daemon = True)
    x.start()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind((HOST, PORT))
        s.listen(1)
        
        while True:
            conn, addr = s.accept()
            
            with conn:
                logging.info('Connected by %s', addr)
                
                while True:
                    data = conn.recv(1024)
                    
                    if not data:
                        break
                        
                    data = data.decode("utf-8")
                    
                    logging.info('Command: %s', data)
                    
                    recv = 'done'
                    
                    if data == "temp":
                        try:
                            recv = str(sensor.readValue())
                        except:
                            recv = "0"
                            
                    if data == "auto-switch-on":
                        autoSwitch = True
                            
                    if data == "auto-switch-off":
                        autoSwitch = False
                        
                    if data == "relay-status":
                        if (relayMode == True and relayExp.readChannel(relayAddr, 0) == 1) or (gpioMode == True and int(gpioObj.getValue()) == 1):
                            recv = "on"
                        else:
                            recv = "off"
                            
                        if autoSwitch == True:
                            recv = recv + ",on"
                        else:
                            recv = recv + ",off"
                            
                    if data == "relay-off":
                        if relayMode == True:
                            relayExp.setChannel(relayAddr, 0, 0)
                            logging.info("Disable the electrical circuit by Relay Expansion")
                        elif gpioMode == True:
                            gpioObj.setValue(0)
                            logging.info("Disable the electrical circuit by GPIO")
                        
                    if data == "relay-on":
                        if relayMode == True:
                            relayExp.setChannel(relayAddr, 0, 1)
                            logging.info("Enable the electrical circuit by Relay Expansion")
                        elif gpioMode == True:
                            gpioObj.setValue(1)
                            logging.info("Enable the electrical circuit by GPIO")
                        
                    conn.sendall(recv.encode())

if __name__ == '__main__':
    __main__()