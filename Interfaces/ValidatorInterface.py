import abc
from ParameterClasses.AuthInfo import AuthInfo
from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.Schema import Schema
from ParameterClasses.DataSetId import DataSetId

class ValidatorInterface(abc.ABC):

    @abc.abstractmethod
    def validateSchema(self, schema:Schema, dataSetID:DataSetId, authToken:AuthToken):
        pass
	
    @abc.abstractmethod
    def getSchema(self, schema:Schema, authInfo:AuthInfo):
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
