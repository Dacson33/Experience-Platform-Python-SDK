class AuthInfo:
	"""
	Holds all the information necessary for authentication to the Adobe Experience Platform.

	Attributes:
		ApiKey (str): The user's aep_sdk Key for the Adobe Experience Platform.
		Username (str): The user's username for the Adobe Experience Platform.
		Password (str): The user's password for the Adobe Experience Platform.
	Quick Methods:
		getApiKey(self):
			Simple getter for apiKey.
		getPassword(self):
			Simple getter for password.
		getUsername(self):
			Simple getter for username.
	"""
	def __init__(self, username, password, apiKey):
		"""
		Constructs all the necessary attributes for an AuthInfo object.

		Args:
			username (str): The user's username for the Adobe Experience Platform.
			password (str): The user's password for the Adobe Experience Platform.
			apiKey (str): The user's aep_sdk Key for the Adobe Experience Platform.
		"""
		self.Username = username
		self.Password = password
		self.ApiKey = apiKey
		
	def getUsername(self):
		"""
		Simple getter for username.

		Returns:
			username (str): The user's username for the Adobe Experience Platform.
		"""
		return self.Username  # String
	
	def getPassword(self):
		"""
		Simple getter for password.

		Returns:
			password (str): The user's password for the Adobe Experience Platform.
		"""
		return self.Password  # String
		
	def getApiKey(self):
		"""
		Simple getter for apiKey.

		Returns:
			apiKey (str): The user's aep_sdk Key for the Adobe Experience Platform.
		"""
		return self.ApiKey  # String
