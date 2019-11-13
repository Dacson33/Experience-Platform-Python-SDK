import abc
from ParameterClasses.AuthInfo import AuthInfo
from ParameterClasses.AuthToken import AuthToken


class SchemaRegistryInterface(abc.ABC):

    @abc.abstractmethod
    def validateSchema(self, schema, authInfo:AuthInfo):
        pass

    @abc.abstractmethod
    def getSchema(self, schemaId, authInfo:AuthInfo):
        pass

    @abc.abstractmethod
    def createSchema(self, authInfo:AuthInfo):
        pass

    @abc.abstractmethod
    def createClass(self, authInfo:AuthInfo):
        pass

    @abc.abstractmethod
    def createMixin(self, authInfo:AuthInfo):
        pass
