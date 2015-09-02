class ClientError(Exception):

	pass

class ConnectionError(ClientError):

	def __init__(self,addr):
		self.addr = addr


class InvalidPort(ClientError):

	def __init__(self,port):
		self.port = port 
		self.msg = 'The port should be a number between 1024 (from 0 to 1024 are occupied) and 65535'

class InvalidUsername(ClientError):

	pass

class LANError(ClientError):

	def __init__(self,ip_addr):
		self.ip_addr = ip_addr
		self.msg = 'Can connect to servers only on your internal network. The IP is 192.168.1.x where x is the ID of the server'