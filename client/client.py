import socket
import client_excep as ex
import threading

class Client(object):

	def __init__(self, ip_addr, port, username):

		self.ip_addr = ip_addr
		self.port = port
		self.username = username
		self.socket = socket.socket()
		self.messages = []


	def start(self):
		try:
			self.socket.connect((self.ip_addr,self.port))
			thread = threading.Thread(target = self.handle_receive)
			thread.daemon = True
			thread.start()
		except socket.error:
			raise ex.ConnectionError('{}:{}'.format(self.ip_addr,self.port))

	def get_credentials(self):
		ip,port = self.socket.getsockname()
		return (self.username,ip,port)

	def handle_receive(self):
		while 1:
			data = self.socket.recv(1024)
			if data:
				self.messages.append(data)
			else:
				continue

	def send(self,message):
		self.socket.sendall(message+'\n')
