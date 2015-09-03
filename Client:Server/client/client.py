import socket
import client_excep as ex
import threading

class Client(object):

	def __init__(self, ip_addr, port, username):

		#server info
		self.ip_addr = ip_addr
		self.port = port
		self.socket = socket.socket()

		self.username = username
		
		#the message list that we use to display the messages and queue them
		self.messages = []


	def start(self):
		try:
			#connecting
			self.socket.connect((self.ip_addr,self.port))
			#send the first packet
			self.socket.send(self.username)
			#receive the first packet, all of this happens in a sequential order
			self.friends_packet = self.socket.recv(1024)
			if self.friends_packet.startswith('USERS'):
				#get the users
				users = self.friends_packet[self.friends_packet.find(':')+1:]
			if users == 'None':
				self.friends = []
			else:
				#self.friends is a list of lists where each child list is a list containing the action and a list of names
				self.friends = [['add',users.split(',')]]
			thread = threading.Thread(target = self.handle_receive)
			#make the thread daemon, so when the mainone hangs this one can respond
			thread.daemon = True
			thread.start()
		except socket.error:
			raise ex.ConnectionError('{}:{}'.format(self.ip_addr,self.port))

	def get_credentials(self):
		#get the creds of the user
		ip,port = self.socket.getsockname()
		return (self.username, ip,port)

	def handle_receive(self):
		while 1:
			data = self.socket.recv(1024)
			if data:
				if data.startswith('USERS'):
					#get the action from the string
					action = data[data.find('(')+1:data.find(')')]
					#append the action and the list of names to the list queue
					self.friends.extend([[action,data[data.find(':')+1:].split(',')]])
					if action == 'add':
						msg = '{} joined the room.\n'.format(data[data.find(':')+1:])
					elif action == 'remove':
						msg = '{} left the room.\n'.format(data[data.find(':')+1:])
					self.messages.append(msg)
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
