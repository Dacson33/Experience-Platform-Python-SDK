from ParameterClasses.AuthToken import AuthToken

class CataloguerInterface:

	def __init__(self):
		pass
	
	def validateSchema(self, schema, datasetID, authToken:AuthToken):
		return None