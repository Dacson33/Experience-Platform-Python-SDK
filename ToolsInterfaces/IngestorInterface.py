import abc


class IngestorInterface(abc.ABC):

    @abc.abstractmethod
    def upload(self, file, schema, dataSetID, authToken):
        pass

    @abc.abstractmethod
    def login(self, authInfo):
        pass
