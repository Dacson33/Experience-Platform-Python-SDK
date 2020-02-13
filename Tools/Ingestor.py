from Interfaces.IngestorInterface import IngestorInterface
from ParameterClasses.Schema import Schema
from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.DataSetId import DataSetId
import requests
import os
import json

class Ingestor(IngestorInterface):

    def __init__(self):
        pass

#    def upload(self, file, schema:Schema, dataSetID:DataSetId, authToken:AuthToken):
#        pass
    def startBatch(self, datasetId, imsOrg, accessToken: AuthToken, apiKey):
        headers = {
            'Content-Type': 'application/json',
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        data = '{\n          "datasetId": "' + datasetId +'",\n           "inputFormat": {\n                "format": "json",\n                "isMultiLineJson": true\n           }\n      }'
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches', headers=headers, data=data)
        print('Create batch status: ' + response.json()['status'])
        batchId = response.json()['id']
        print(batchId)
        return batchId

    def sendFile(self, fileName, batchId, datasetId, imsOrg, accessToken: AuthToken, apiKey):
        headers = {
            'Content-Type': 'application/octet-stream',
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        print('File upload of ' + os.path.basename(fileName) + ' in progress')
        file = open(fileName, 'rb')
        data = file.read()
        file.close()
        #print(data)
        response = requests.put(
            'https://platform.adobe.io/data/foundation/import/batches/' + batchId + '/datasets/' + datasetId + '/files/' + os.path.basename(
                fileName), headers=headers, data=data)
        return response

    def finishUpload(self, batchId, imsOrg, accessToken: AuthToken, apiKey, cataloguer):
        headers = {
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        params = (
            ('action', 'COMPLETE'),
        )
        print('Signal Completion: ')
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches/' + batchId, headers=headers,
                                 params=params)
        if not self.error_check(response):
            print("Signal Completion has failed for " + batchId)
        else:
            print(batchId + " upload completed successfully")
        return cataloguer.report(batchId, imsOrg, accessToken, apiKey)

    def upload(self, fileName, batchId, datasetId, imsOrg, accessToken:AuthToken, apiKey, cataloguer):
        #batchId = self.startBatch(datasetId, imsOrg, accessToken, apiKey)
        #Uploads the file
        response = self.sendFile(fileName, batchId, datasetId, imsOrg, accessToken, apiKey)
        if not self.error_check(response):
            return
        #Signals the completion of the batch
        #return self.finishUpload(fileName, batchId, imsOrg, accessToken, apiKey, cataloguer)
        #return batchId

    def uploadLarge(self, fileName, batchId, datasetId, imsOrg, accessToken:AuthToken, apiKey, cataloguer):
        #batchId = self.startBatch(datasetId, imsOrg, accessToken, apiKey)
        self.new_split(fileName)
        for entry in os.scandir('Splits/'):
            response = self.sendFile(entry.path, batchId, datasetId, imsOrg, accessToken, apiKey)
            if not self.error_check(response):
                print(os.path.basename(entry.path) + ' failed to upload')
                continue
            os.remove(entry.path)
        os.rmdir('Splits/')
        #return self.finishUpload(fileName, batchId, imsOrg, accessToken, apiKey, cataloguer)
        #return batchId

    def error_check(self, response):
        if response.status_code != 200:
            print("Error: " + response.status_code)
            return False
        return True

    def _one_pass(self, iters):
        i = 0
        while i < len(iters):
            try:
                yield next(iters[i])
            except StopIteration:
                del iters[i]
            else:
                i += 1

    def zip_varlen(self, *iterables):
        iters = [iter(it) for it in iterables]
        while True:  # broken when an empty tuple is given by _one_pass
            val = tuple(self._one_pass(iters))
            if val:
                yield val
            else:
                break

    def grouper(self, iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        args = [iter(iterable)] * n
        #return zip_longest(fillvalue=fillvalue, *args)
        return self.zip_varlen(*args)

    def new_split(self, fileName):
        file = open(fileName, 'rb')
        values = file.read()
        file.close()
        #values = values.replace('\n', '')
        #v = values.encode('utf-8')
        v = json.loads(values)
        os.mkdir('Splits/')
        for i, group in enumerate(self.grouper(v, 125000)):
            with open('Splits/' + os.path.splitext(os.path.basename(fileName))[0] + '_{}.json'.format(i), 'w') as outputfile:
                json.dump(list(group), outputfile)
        #for entry in os.scandir('Splits/'):
            #os.remove(entry.path)
        #os.rmdir('Splits/')
