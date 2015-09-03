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
		self.counter = 0

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
			#use the sender host id and port as keys and his username and and address as values
			key = '{}:{}'.format(addr[0].split('.')[-1], addr[1])
			#get the username
			username = self.connections[addr].recv(1024)
			#if the usernameis already in the dict add 1 to it
			for user in self.users:
				if username == self.users[user][0]:
					username += str(self.counter)
					self.counter += 1
			#send all users before appending the current user or None if he is the first to enter the room
			if self.users:
				users = [value[0] for value in self.users.values()]
				users = ','.join(users)
				users_packet = 'USERS(add):{}'.format(users)
				self.connections[addr].sendall(users_packet)
			else:
				self.connections[addr].sendall('USERS:None')
			#send the new user to the rest of the users
			self.broadcast('USERS(add):{}'.format(username),addr)
			#save the username and addr
			self.users[key] = username,addr
			#start the thread to handle this client
			thread = threading.Thread(target=self.handle_client,args = (addr,))
			thread.start()
			#log the new connection
			self.events.append('A new connection from ({}), starting a new thread\n'.format(addr))

	def handle_client(self,addr):
		while 1:
			try:
				#receive some data
				data = self.connections[addr].recv(1024)
				if data:
					#get the key for the username dict
					sender_id = '{}:{}'.format(addr[0].split('.')[-1],addr[1])
					if data.startswith('MSG'):
						#if its a noemal message, we prepare it and broadcast it to everyone
						msg = '{}: {}'.format(self.users[sender_id][0],data[data.find(':')+1:])
						self.broadcast(msg,addr)
					elif data.startswith('PRIVATE'):
						#if its a private message, we prepare the message and get the receiver's address from his username
						#if we encounter an IndexError, that means that there is no such user in the room
						#we send an error message to the sender
						try:
							receiver = [value[1] for value in self.users.values() if value[0] == data[data.find('(')+1: data.find(')')]][0]
							msg = 'PRIVATE {}: {}'.format(self.users[sender_id][0],data[data.find(':')+1:])
						except IndexError:
							receiver = self.users[sender_id][1]
							msg = 'ERROR: The user you tried to message is not online\n'
						self.broadcast(msg,addr,receiver)
					elif data.startswith('QUIT'):
						#if the user sends quit, we delete his socket, broadcast the leaving message
						# and send the info to the rest so they can delete him from their list
						msg = 'USERS(remove):{}'.format(self.users[sender_id][0])
						self.broadcast(msg,addr)
						del self.connections[addr]
			#if a KeyError occurs, that means that the client socket has already closed the connection
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