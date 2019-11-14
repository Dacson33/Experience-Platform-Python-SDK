import abc
from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.DataSetId import DataSetId
from ParameterClasses.Schema import Schema

class IngestorInterface(abc.ABC):

    @abc.abstractmethod
    def upload(self, file, schema:Schema, dataSetID:DataSetId, authToken:AuthToken):
        pass #File is fileInputScheme
