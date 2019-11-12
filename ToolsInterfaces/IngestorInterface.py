import abc
from ParameterClasses.AuthToken import AuthToken


class IngestorInterface(abc.ABC):

    @abc.abstractmethod
    def upload(self, file, schema, dataSetID, authToken:AuthToken):
        pass

