class AuthToken:
	def __init__(self,token,expiration,expirationDate):
		self.Token = token
		self.Expiration = expiration
		self.ExpirationDate = expirationDate
	
	def getToken(self):
		return self.Token #String
	
	def getExpiration(self):
		return self.Expiration #Date

	def getExpirationDate(self):
		return self.ExpirationDate
