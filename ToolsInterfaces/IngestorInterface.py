import abc


class IngestorInterface(abc.ABC):
    @abc.abstractmethod
    def upload(self):
        pass

    @abc.abstractmethod
    def login(self):
        pass
