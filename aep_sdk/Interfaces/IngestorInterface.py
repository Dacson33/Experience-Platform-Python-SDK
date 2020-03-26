import abc

from aep_sdk.ParameterClasses.AuthToken import AuthToken


class IngestorInterface(abc.ABC):

    @abc.abstractmethod
    def upload(self, file_name, batch_id, dataset_id, ims_org, access_token: AuthToken, api_key):
        pass
#   def upload(self, file, schema:Schema, dataSetID:DataSetId, authToken:AuthToken):
#       pass #File is fileInputScheme
