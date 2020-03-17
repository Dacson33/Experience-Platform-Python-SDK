from aep_sdk.Interfaces import IngestorInterface
from aep_sdk.ParameterClasses.AuthToken import AuthToken
import requests
import os
import json

class Ingestor(IngestorInterface.IngestorInterface):
    """
    An object that handles the uploading of files to the Adobe Experience Platform.

    Quick Methods:
        error_check(self, response):
            A function that checks if a response object was valid.
        finishUpload(self, batchId, imsOrg, accessToken: AuthToken, apiKey, cataloguer):
            A function that signals the completion of the batch.
        new_split(self, fileName):
            A function that splits up JSON files of sizes greater than 256MB.
        sendFile(self, fileName, batchId, datasetId, imsOrg, accessToken: AuthToken, apiKey):
            A function that sends the file to a batch to be uploaded.
        startBatch(self, datasetId, imsOrg, accessToken: AuthToken, apiKey):
            A function that creates the batch that the files will upload to.
        upload(self, fileName, batchId, datasetId, imsOrg, accessToken:AuthToken, apiKey, cataloguer):
            A function that handles the uploading of files of sizes less than or equal to 256MB.
        uploadLarge(self, fileName, batchId, datasetId, imsOrg, accessToken:AuthToken, apiKey, cataloguer):
            A function that handles the uploading of files of sizes greater than 256MB.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for an Ingestor object.
        """
        pass

#    def upload(self, file, schema:Schema, dataSetID:DataSetId, authToken:AuthToken):
#        pass
    def startBatch(self, datasetId, imsOrg, accessToken: AuthToken, apiKey):
        """
        A function that creates the batch that the files will upload to.

        Args:
            datasetId (str): The string that is the dataset ID that is being uploaded to.
            imsOrg (str): The IMS Organization email of the user.
            accessToken (AuthToken): The user's current active authorization token.
            apiKey (str): The user's aep_sdk Key for the Adobe Experience Platform.

        Returns:
            batchId (str): A string that is the id of the batch that has just been created.
        """

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
        """
        A function that sends the file to a batch to be uploaded.

        Args:
            fileName (str): The full name and path of the file to be uploaded.
            batchId (str): The id of the batch that the file is being sent to.
            datasetId (str): The id of the dataset that is being uploaded to.
            imsOrg (str): The IMS Organization email of the user.
            accessToken (AuthToken): The user's current active authorization token.
            apiKey (str): The user's aep_sdk Key for the Adobe Experience Platform.

        Returns:
            response (Response): The response object given by the put request to the Adobe Experience Platform.
        """

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
        """
        A function that signals the completion of the batch.

        Args:
            batchId (str): The id of the batch currently being uploaded.
            imsOrg (str): The IMS Organization email of the user.
            accessToken (AuthToken): The user's current active authorization token.
            apiKey (str): The user's aep_sdk Key for the Adobe Experience Platform.
            cataloguer (Cataloguer): A Cataloguer object used for reporting the batch status.

        Returns:
            status (str): The string of the batch status given by the cataloguer's report function.
        """

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
        """
        A function that handles the uploading of files of sizes less than or equal to 256MB.

        Args:
            fileName (str): The full name and path of the file being uploaded.
            batchId (str): The id of the batch that is being used.
            datasetId (str): The id of the dataset that is being uploaded to.
            imsOrg (str): The IMS Organization email of the user.
            accessToken (AuthToken): The user's current active authorization token.
            apiKey (str): The user's aep_sdk Key for the Adobe Experience Platform.
        """

        #batchId = self.startBatch(datasetId, imsOrg, accessToken, apiKey)
        #Uploads the file
        response = self.sendFile(fileName, batchId, datasetId, imsOrg, accessToken, apiKey)
        if not self.error_check(response):
            return
        #Signals the completion of the batch
        #return self.finishUpload(fileName, batchId, imsOrg, accessToken, apiKey, cataloguer)
        #return batchId

    def uploadLarge(self, fileName, batchId, datasetId, imsOrg, accessToken:AuthToken, apiKey, cataloguer):
        """
        A function that handles the uploading of files of sizes greater than 256MB.

        Args:
            fileName (str): The full name and path of the file being uploaded.
            batchId (str): The id of the batch that is being used.
            datasetId (str): The id of the dataset that is being uploaded to.
            imsOrg (str): The IMS Organization email of the user.
            accessToken (AuthToken): The user's current active authorization token.
            apiKey (str): The user's aep_sdk Key for the Adobe Experience Platform.
        """

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
        """
        A function that checks if a response object was valid.

        Args:
            response (Response): A response object from the requests library.

        Returns:
            valid (bool): A boolean stating whether there was an error code or not.
        """

        if response.status_code != 200:
            print("Error: " + response.status_code)
            return False
        return True

    def _one_pass(self, iters):
        """
        Helper for the new_split function.
        """
        i = 0
        while i < len(iters):
            try:
                yield next(iters[i])
            except StopIteration:
                del iters[i]
            else:
                i += 1

    def zip_varlen(self, *iterables):
        """
        Helper for the new_split function.
        """
        iters = [iter(it) for it in iterables]
        while True:  # broken when an empty tuple is given by _one_pass
            val = tuple(self._one_pass(iters))
            if val:
                yield val
            else:
                break

    def grouper(self, iterable, n, fillvalue=None):
        """
        Helper for the new_split function.
        """
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        args = [iter(iterable)] * n
        #return zip_longest(fillvalue=fillvalue, *args)
        return self.zip_varlen(*args)

    def new_split(self, fileName):
        """
        A function that splits up JSON files of sizes greater than 256MB.

        Args:
            fileName: The full name and path of the file being split.
        """

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
