import socket
import threading
import server_excep as ex

class ChatServer(object):

	def __init__(self,port):

		self.socket = socket.socket()
		self.ip_addr = socket.gethostbyname(socket.getfqdn())
		self.port = port
		self.connections = {}
		self.users = {}
		self.events = []

	def start_server(self):
		try:
			self.socket.bind((self.ip_addr,self.port))
			self.socket.listen(5)
			self.listen_thread = threading.Thread(target = self.listen_clients)
			self.listen_thread.daemon = True
			self.listen_thread.start()
		except socket.error:
			raise ex.ConnectionError()


	def listen_clients(self):

		while 1:
			conn, addr = self.socket.accept()
			self.connections[addr] = conn
			key = int(addr[0].split('.')[-1])
			username = self.connections[addr].recv(1024)
			self.users[key] = username
			thread = threading.Thread(target=self.handle_client,args = (addr,))
			thread.start()
			self.events.append('A new connection from ({}), starting a new thread\n'.format(addr))

	def handle_client(self,addr):
		while 1:
			data = self.connections[addr].recv(1024)
			if data:
				username = int(addr[0].split('.')[-1])
				msg = '{}: {}'.format(self.users[username],data)
				for address in self.connections:
					if address != addr:
						self.connections[address].sendall(msg)

	def stop_server(self):
		self.socket.close()

	def get_event(self):
		return self.events.pop(0)