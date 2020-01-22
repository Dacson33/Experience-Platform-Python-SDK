from Interfaces.IngestorInterface import IngestorInterface
from ParameterClasses.Schema import Schema
from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.DataSetId import DataSetId
import requests
import os
from bitmath import MiB
from fsplit.filesplit import FileSplit

class Ingestor(IngestorInterface):

    def __init__(self):
        pass

#    def upload(self, file, schema:Schema, dataSetID:DataSetId, authToken:AuthToken):
#        pass

    def upload(self, fileName, datasetId, imsOrg, accessToken:AuthToken, apiKey, cataloguer):
        #Creates the batch
        headers = {
            'Content-Type': 'application/json',
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        data = '{ \n          "datasetId": "'+datasetId+'" \n      }'
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches', headers=headers, data=data)
        print('Create batch status: ' + response.json()['status'])
        batchId = response.json()['id']
        #Uploads the file
        headers = {
            'Content-Type': 'application/octet-stream',
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        print('File upload of ' + os.path.basename(fileName) + ' in progress')
        #data = open('Tests/' + fileName, 'rb').read()
        data = open(fileName, 'rb').read()
        response = requests.put('https://platform.adobe.io/data/foundation/import/batches/' + batchId + '/datasets/' + datasetId + '/files/' + os.path.basename(fileName), headers=headers, data=data)
        print(response)
        #Signals the completion of the batch
        headers = {
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        params = (
            ('action', 'COMPLETE'),
        )
        print('Signal Completion: ')
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches/' + batchId, headers=headers, params=params)
        print(response)
        cataloguer.report(batchId, imsOrg, accessToken, apiKey)

    def uploadLarge(self, fileName, dataSetId, imsOrg, accessToken:AuthToken, apiKey, cataloguer):
        headers = {
            'Content-Type': 'application/json',
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        data = '{ \n          "datasetId": "' + dataSetId + '" \n      }'
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches', headers=headers, data=data)
        print('Create batch status: ' + response.json()['status'])
        batchId = response.json()['id']
        fs = FileSplit(file=fileName, splitsize=256000000, output_dir='Splits/')
        fs.split(include_header=True)
        for entry in os.scandir('Splits/'):
            print(entry.path)
            headers = {
                'Content-Type': 'application/octet-stream',
                'x-gw-ims-org-id': imsOrg,
                'Authorization': 'Bearer ' + accessToken.getToken(),
                'x-api-key': apiKey
            }
            print('File upload of ' + os.path.basename(entry.path) + ' in progress')
            data = open(entry.path, 'rb').read()
            response = requests.put(
                'https://platform.adobe.io/data/foundation/import/batches/' + batchId + '/datasets/' + dataSetId + '/files/' + os.path.basename(entry.path),
                headers=headers, data=data)
            print(response)
            os.remove(entry.path)

        headers = {
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        params = (
            ('action', 'COMPLETE'),
        )
        print('Signal Completion: ')
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches/' + batchId,
                                 headers=headers, params=params)
        print(response)
        cataloguer.report(batchId, imsOrg, accessToken, apiKey)
