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
			self.socket.send(self.username)
			self.friends_packet = self.socket.recv(1024)
			if self.friends_packet.startswith('USERS'):
				users = self.friends_packet[self.friends_packet.find(':')+1:]
			if users == 'None':
				self.friends = []
			else:
				self.friends = [['add',users.split(',')]]
			thread = threading.Thread(target = self.handle_receive)
			thread.daemon = True
			thread.start()
		except socket.error:
			raise ex.ConnectionError('{}:{}'.format(self.ip_addr,self.port))

	def get_credentials(self):
		ip,port = self.socket.getsockname()
		return (self.username, ip,port)

	def handle_receive(self):
		while 1:
			data = self.socket.recv(1024)
			if data:
				if data.startswith('USERS'):
					action = data[data.find('(')+1:data.find(')')]
					self.friends.extend([action,[data[data.find(':')+1:].split(',')]])
				else:
					self.messages.append(data)
			else:
				continue

	def send(self,message):
		if message.startswith('/w'):
			user = message.split()[1]
			data = ' '.join(message.split()[2:])
			new_message = 'PRIVATE({}):{}\n'.format(user,data)
		else:
			new_message = 'MSG: ' + message +'\n'
		self.socket.sendall(new_message)


	def quit(self):
		self.socket.sendall('QUIT')
		self.socket.close()
