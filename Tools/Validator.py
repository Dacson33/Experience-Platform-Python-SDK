from Interfaces.ValidatorInterface import ValidatorInterface
from ParameterClasses.AuthInfo import AuthInfo
from ParameterClasses.AuthToken import AuthToken

class Validator(ValidatorInterface):
    def __init__(self):
        pass

    def validateSchema(self, schema, authInfo:AuthInfo):
        pass

    def getSchema(self, schemaId, authInfo:AuthInfo):
        pass

    def createSchema(self, authInfo:AuthInfo):
        pass

    def createClass(self, authInfo:AuthInfo):
        pass

    def createMixin(self, authInfo:AuthInfo):
        pass