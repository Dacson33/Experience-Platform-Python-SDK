import abc
from ParameterClasses.AuthInfo import AuthInfo
from ParameterClasses.AuthToken import AuthToken


class IngestorInterface(abc.ABC):

    @abc.abstractmethod
    def upload(self, file, schema, dataSetID, authToken:AuthToken):
        pass

    @abc.abstractmethod
    def login(self, authInfo:AuthInfo):
        pass
