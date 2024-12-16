import serial 
import time 

port = "/dev/ttyACM0" 

baudrate = 115200 

serial_connection = serial.Serial(port, baudrate) 


def send(data) :
	data=data.encode() # data in bytes
	 
	serial_connection.write(data)

time.sleep(0.01) 





