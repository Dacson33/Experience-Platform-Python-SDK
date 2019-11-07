class AuthInfo:
	def __init__(self,username, password, apiKey):
		self.Username = username
		self.Password = password
		self.ApiKey = apiKey
		
	def getUsername(self):
		return self.Username
	
	def getPassword(self):
		return self.Password
		
	def getApiKey(self):
		return self.ApiKey