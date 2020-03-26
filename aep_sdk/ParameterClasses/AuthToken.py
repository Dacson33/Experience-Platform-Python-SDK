import datetime


class AuthToken:
	"""
	Holds all the information about an Authentication Token for the Adobe Experience Platform.

	Attributes:
		token (str): The actual token used for authentication.
		expiration (int): The number of milliseconds this token is valid for.
		expiration_date (datetime.pyi): The datetime that this token expires.
	Quick Methods:
		get_expiration(self):
			Simple getter for expiration.
		get_expirationDate(self):
			Simple getter for expiration_date.
		get_token(self):
			Simple getter for token.
	"""
	def __init__(self, token, expiration, expiration_date):
		"""
		Constructs all the necessary attributes for an AuthToken object.

		Args:
			token (str): The actual token used for authentication.
			expiration (int): The number of milliseconds this token is valid for.
			expiration_date (datetime.pyi): The datetime that this token expires.
		"""
		self.token = token
		self.expiration = expiration
		self.expiration_date = expiration_date
	
	def get_token(self):
		"""
		Simple getter for token.

		Returns:
			token (str): The actual token used for authentication.
		"""
		return self.token
	
	def get_expiration(self):
		"""
		Simple getter for expiration.

		Returns:
			expiration (int): The number of milliseconds this token is valid for.
		"""
		return self.expiration

	def get_expiration_date(self):
		"""
		Simple getter for expiration_date.

		Returns:
			expiration_date (datetime.pyi): The datetime that this token expires.
		"""
		return self.expiration_date
