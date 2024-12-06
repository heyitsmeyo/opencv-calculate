import socket 


host = "192.168.150.39"
port = 3030 

def send(y) :
	y = y.encode()
	with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s : 
		s.connect((host, port))
		s.sendall(y)
	
	


