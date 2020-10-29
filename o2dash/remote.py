import socket
import time

host = '0.0.0.0' # IP address of Omega2(+) or Omega2 Pro with temperature sensor
port = 50005

def sendCommand(command = "stat"):
	addr = socket.getaddrinfo(host, port)[0][-1]
	
	s = socket.socket()
	s.settimeout(5.0)
	
	try:
		s.connect(addr)
	except:
		return False
		
	s.send(command)
	
	try:
		data = s.recv(1024)
	except:
		print("Socket recv problem.")
	
	s.close()
	return data
	
def checkRemote():
	temp = checkTempSensor()
	(relayStatus, relayAuto) = checkRelay()
	return (temp, relayStatus, relayAuto)
	
def checkTempSensor():
	print("Checking sensor value...")
	
	recv = sendCommand('temp')
	
	if recv:
		value = int(float(recv.decode()))
	else:
		value = 0
		
	return value
	
def checkRelay():
	print("Checking relay status...")
	
	recv = sendCommand('relay-status')
	
	if recv:
		r = recv.decode()
		r = r.split(",")
		try:
			return(True if r[0] == 'on' else False, True if r[1] == 'on' else False)
		except:
			return (False, False)
	else:
		return (False, False)
	
def switchRelay(command = 'relay-off'):
	print("Switching relay...")
	
	recv = sendCommand(command)
	if recv:
		r = recv.decode()
		if r == 'done':
			return True
		else:
			return False
	else:
		return False