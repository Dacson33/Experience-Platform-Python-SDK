import abc
from aep_sdk.ParameterClasses.AuthToken import AuthToken
from aep_sdk.ParameterClasses.DataSetId import DataSetId


class IngestorInterface(abc.ABC):

    @abc.abstractmethod
    def upload(self, fileName, batchId, datasetId: DataSetId, imsOrg, accessToken: AuthToken, apiKey, cataloguer):
        pass
#   def upload(self, file, schema:Schema, dataSetID:DataSetId, authToken:AuthToken):
#       pass #File is fileInputScheme
