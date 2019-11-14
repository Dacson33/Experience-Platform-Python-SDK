class AuthInfo:
	def __init__(self, username, password, apiKey):
		self.Username = username
		self.Password = password
		self.ApiKey = apiKey
		
	def getUsername(self):
		return self.Username #String
	
	def getPassword(self):
		return self.Password #String
		
	def getApiKey(self):
		return self.ApiKey #String