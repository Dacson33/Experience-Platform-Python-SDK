from Interfaces.IngestorInterface import IngestorInterface
from ParameterClasses.Schema import Schema
from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.DataSetId import DataSetId


class Ingestor(IngestorInterface):

    def __init__(self):
        pass

    def upload(self, file, schema:Schema, dataSetID:DataSetId, authToken:AuthToken):
        pass

