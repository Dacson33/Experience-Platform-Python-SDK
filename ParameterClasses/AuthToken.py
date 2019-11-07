class AuthToken:
	def __init__(self,token,expiration):
		self.Token = token
		self.Expiration = Expiration
	
	def getToken(self):
		return self.Token
	
	def getExpiration(self):
		return self.Expiration