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
			#accept a connection
			conn, addr = self.socket.accept()
			#save the connection socket
			self.connections[addr] = conn
			#use the sender host id to save his username
			key = '{}:{}'.format(addr[0].split('.')[-1], addr[1])
			#get the username , which is the first thing that the client sends
			username = self.connections[addr].recv(1024)
			#send all users before appending the current user
			if self.users:
				users = [value[0] for value in self.users.values()]
				users = ','.join(users)
				users_packet = 'USERS(add):{}'.format(users)
				self.connections[addr].sendall(users_packet)
			else:
				self.connections[addr].sendall('USERS:None')
			self.broadcast('{} joined the room\n'.format(username),addr)
			#save the username
			self.users[key] = username,addr
			#start the thread to handle this client
			thread = threading.Thread(target=self.handle_client,args = (addr,))
			thread.start()
			#log the new connection
			self.events.append('A new connection from ({}), starting a new thread\n'.format(addr))

	def handle_client(self,addr):
		while 1:
			try:
				data = self.connections[addr].recv(1024)
				if data:
					sender_id = '{}:{}'.format(addr[0].split('.')[-1],addr[1])
					if data.startswith('MSG'):
						msg = '{}: {}'.format(self.users[sender_id][0],data[data.find(':')+1:])
						self.broadcast(msg,addr)
					elif data.startswith('PRIVATE'):
						try:
							receiver = [value[1] for value in self.users.values() if value[0] == data[data.find('(')+1: data.find(')')]][0]
							msg = 'PRIVATE {}: {}'.format(self.users[sender_id][0],data[data.find(':')+1:])
						except IndexError:
							receiver = self.users[sender_id][1]
							msg = 'ERROR: The user you tried to message is not online\n'
						self.broadcast(msg,addr,receiver)
					elif data.startswith('QUIT'):
						msg = '{} left the room\n'.format(self.users[sender_id][0])
						self.broadcast(msg,addr)
						msg2 = 'USERS(remove):{}'.format(self.users[sender_id][0])
						del self.connections[addr]
			except KeyError:
				break




	def broadcast(self,msg,sender,to=None):
		if to == None:
			for connection in self.connections:
				if connection != sender:
					self.connections[connection].sendall(msg)
		else:
			self.connections[to].sendall(msg)


	def stop_server(self):
		self.socket.close()

	def get_event(self):
		return self.events.pop(0)