from ParameterClasses.AuthInfo import AuthInfo
from ParameterClasses.AuthToken import AuthToken
from ToolsInterfaces.SchemaRegistryInterface import SchemaRegistryInterface


class SchemaRegistry(SchemaRegistryInterface):

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
