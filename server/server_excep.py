class ServerErrors(Exception):

	pass

class WrongIPAddress(ServerErrors):

	def __init__(self,ip_addr):
		self.ip_addr = ip_addr
		self.msg = 'The IP address should be in the form x.x.x.x where x is a number from 0 to 255'

class WrongPort(ServerErrors):

	def __init__(self,port):
		self.port = port
		self.msg = 'The port should be a number between 1024 (from 0 to 1024 are occupied) and 65535'

		