from Interfaces.ValidatorInterface import ValidatorInterface
from ParameterClasses.AuthInfo import AuthInfo
from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.Schema import Schema

class Validator(ValidatorInterface):
    def __init__(self):
        pass

    def validateSchema(self, schema:Schema, authInfo:AuthInfo):
        pass

    def getSchema(self, schema:Schema, authInfo:AuthInfo):
        pass

    def createSchema(self, authInfo:AuthInfo):
        pass

    def createClass(self, authInfo:AuthInfo):
        pass

    def createMixin(self, authInfo:AuthInfo):
        pass
