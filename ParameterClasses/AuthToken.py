class AuthToken:
	"""
	Holds all the information about an Authentication Token for the Adobe Experience Platform.

	Attributes:
		token (str): The actual token used for authentication.
		expiration (int): The number of milliseconds this token is valid for.
		expirationDate (datetime): The datetime that this token expires.
	Quick Methods:
		getExpiration(self):
			Simple getter for expiration.
		getExpirationDate(self):
			Simple getter for expirationDate.
		getToken(self):
			Simple getter for token.
	"""
	def __init__(self, token, expiration, expirationDate):
		"""
		Constructs all the necessary attributes for an AuthToken object.

		Args:
			token (str): The actual token used for authentication.
			expiration (int): The number of milliseconds this token is valid for.
			expirationDate (datetime): The datetime that this token expires.
		"""
		self.Token = token
		self.Expiration = expiration
		self.ExpirationDate = expirationDate
	
	def getToken(self):
		"""
		Simple getter for token.

		Returns:
			token (str): The actual token used for authentication.
		"""
		return self.Token
	
	def getExpiration(self):
		"""
		Simple getter for expiration.

		Returns:
			expiration (int): The number of milliseconds this token is valid for.
		"""
		return self.Expiration

	def getExpirationDate(self):
		"""
		Simple getter for expirationDate.

		Returns:
			expirationDate (datetime): The datetime that this token expires.
		"""
		return self.ExpirationDate
