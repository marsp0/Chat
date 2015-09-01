class ServerError(Exception):

	pass

class InvalidPort(ServerError):

	def __init__(self,port):
		self.port = port
		self.msg = 'The port should be a number between 1024 (from 0 to 1024 are occupied) and 65535'

class ConnectionError(ServerError):
	pass