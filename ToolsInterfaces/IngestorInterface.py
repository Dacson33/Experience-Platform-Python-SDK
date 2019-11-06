import abc

class IngestorInterface(abc.ABC):
    @abc.abstractmethod
    def Upload(self):
        pass