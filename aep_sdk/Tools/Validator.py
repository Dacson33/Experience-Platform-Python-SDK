from aep_sdk.Interfaces import ValidatorInterface
from aep_sdk.ParameterClasses import AuthInfo
from aep_sdk.ParameterClasses import Schema


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
