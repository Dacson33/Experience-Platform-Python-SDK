import abc
from aep_sdk.ParameterClasses import AuthInfo
from aep_sdk.ParameterClasses.AuthToken import AuthToken
from aep_sdk.ParameterClasses import Schema
from aep_sdk.ParameterClasses.DataSetId import DataSetId


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
