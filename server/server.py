import socket
import threading

class Server(object):

	def __init__(self,ip_address,port):

		self.socket = socket.socket()
		self.connections = {}
		self.start_server(ip_address,port)

	def start_server(self,ip_addr,port):
		self.socket.bind((ip_addr,port))
		self.socket.listen(5)
		self.listen()

	def listen(self):
		while 1:
			connection, addr = self.socket.accept()
			self.connections[addr] = connection
			self.handle_thraed = threading.Thread(target=self.handle_client,(addr,))
			self.handle_thraed.start()

	def handle_client(self,addr):
		while 1:
			data = self.connections[addr].recv(1024)
			if data:
				print data
			else:
				continue
