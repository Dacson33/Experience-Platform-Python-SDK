import requests
import json
import jwt
import datetime
import os
from bitmath import MiB
from ParameterClasses.AuthToken import AuthToken
from Tools.Cataloguer import Cataloguer
from Tools.Ingestor import Ingestor

class API:
    """
    The handler for the entire SDK.

    Attributes:
        accessToken (AuthToken): The user's current active authorization token.
        apiKey (str): The user's API Key for the Adobe Experience Platform.
        aud (str): The audience for the JWT token.
        cataloguer (Cataloguer): A Cataloguer object used for reporting.
        clientSecret (str): The client_secret id of the user.
        imsOrg (str): The IMS Organization email of the user.
        ingestor (Ingestor): An Ingestor object used for the handling of uploading files.
        jwtToken (str): The current JWT token.
        secret (str): The user's secret key used for the creation of JWT tokens.
        sub (str): The user's Technical Account id for Adobe I/O.

    Quick Methods:
        access(self):
            A function that generates and Auth Token for the current user.
        dataId(self):
            A function that queries and returns a list of datasets that are assigned to the current user.
        initConfig(self, configFile):
            A function that initializes the config file and checks it for errors.
        report(self, identification):
            Runs the cataloguer report function, which will wait until the batch finishes loading before printing the batch status.
        upload(self, files, datasetId):
            A function which uploads the given files to the given dataset ID using the ingestor.
        validate(self, dataSetID):
            A function that checks if a given dataset ID exists for the current account.
    """

    def __init__(self, configFile):
        """
        Constructs all the necessary attributes for an API object.

        Args:
            configFile (str): The full name and path of the config file.
        """
        if not self.initConfig(configFile):
            print("Bad config file")
            exit(0)
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600),
            "iss": self.imsOrg,
            "sub": self.sub,
            "https://ims-na1.adobelogin.com/s/ent_dataservices_sdk": True,
            "aud": self.aud
        }
        self.jwtToken = jwt.encode(payload, self.secret, algorithm='RS256').decode('utf-8')
        self.accessToken = self.access()
        self.cataloguer = Cataloguer()
        self.ingestor = Ingestor()

    def initConfig(self, configFile):
        """
        A function that initializes the config file and checks it for errors.

        Args:
            configFile (str): The full name and path of the config file.

        Returns:
            initialized (bool): A boolean stating if the config was successfully initialized or not.
        """

        with open(configFile) as json_data_file:
            data = json.load(json_data_file)
        if not data.get('api_key'):
            return False
        self.apiKey = data['api_key']
        if not self.validateString(self.apiKey):
            return False
        if not data.get('client_secret'):
            return False
        self.clientSecret = data['client_secret']
        if not self.validateString(self.clientSecret):
            return False
        if not data.get('dataID'):
            return False
        if not data.get('ims_org'):
            return False
        self.imsOrg = data['ims_org']
        if not self.validateString(self.imsOrg):
            return False
        if not data.get('sub'):
            return False
        self.sub = data['sub']
        if not self.validateString(self.sub):
            return False
        if not data.get('secret'):
            return False
        self.secret = data['secret']
        if not self.validateString(self.secret):
            return False
        self.aud = 'https://ims-na1.adobelogin.com/c/' + self.apiKey
        return True

    def validateString(self, obj):
        """
        A helper function for initConfig that sees if an object from the config json file is not null or an empty string.

        Args:
            obj (str): The string we are validating.

        Returns:
            valid (bool): A boolean stating if the object was null/empty or not.
        """
        if obj is None or obj == "":
            return False
        return True

    def report(self, identification):
        """
        Runs the cataloguer report function, which will wait until the batch finishes loading before printing the batch status.

        Args:
            identification (str): The dataset ID of the batch to report on.
        """
        self.cataloguer.report(identification, self.imsOrg, self.accessToken, self.apiKey)

    def validate(self, dataSetID):
        """
        A function that checks if a given dataset ID exists for the current account.

        Args:
            dataSetID (str): A dataset ID to validate.

        Returns:
            exists (bool): A boolean stating whether the dataset ID exists on the current account.
        """
        if dataSetID == "":
            print("You need to enter a DataSetID.")
            return False
        headers = {
            'Authorization': 'Bearer ' + self.accessToken.getToken(),
            'x-api-key': self.apiKey,
            'x-gw-ims-org-id': self.imsOrg,
        }
        params = (
            ('properties', 'name,description,state,tags,files'),
        )
        response = requests.get('https://platform.adobe.io/data/foundation/catalog/dataSets/' + dataSetID,
                                headers=headers, params=params)
        if not self.error_checkJson(response):
            return False
        return True

    def access(self):
        """
        A function that generates and Auth Token for the current user.

        Returns:
            authorization (AuthToken): An valid authorization token for the current user that will last for 24 hours.
        """
        files = {
            'client_id': (None, self.apiKey),
            'client_secret': (None, self.clientSecret),
            'jwt_token': (None, self.jwtToken),
        }
        testData = requests.post('https://ims-na1.adobelogin.com/ims/exchange/jwt/', files=files)
        if not self.error_checkJson(testData):
            exit(0)
        name = testData.json()['access_token']
        expiration = testData.json()['expires_in']
        expirationDate = datetime.datetime.utcnow() + datetime.timedelta(milliseconds=expiration - 1000)
        authorization = AuthToken(name, expiration, expirationDate)
        return authorization

    def dataId(self):
        """
        A function that queries and returns a list of datasets that are assigned to the current user.

        Returns:
            datasetIDs (list): A list of dataset ID's belonging to the current account.
        """
        headers = {
            'Authorization': 'Bearer ' + self.accessToken.getToken(),
            'x-api-key': self.apiKey,
            'x-gw-ims-org-id': self.imsOrg,
        }
        params = (
            ('limit', '5'),
            ('properties', 'name'),
        )
        response = requests.get('https://platform.adobe.io/data/foundation/catalog/dataSets', headers=headers, params=params)
        ids = []
        if not self.error_checkJson(response):
            exit(0)
        for id in response.json():
            ids.append(id)
        return ids

    def upload(self, files, datasetId):
        """
        A function which uploads the given files to the given dataset ID using the ingestor.

        Args:
            files (list): A list of strings which are the full path and names of the files being uploaded.
            datasetId (str): The dataset ID that is being uploaded to.

        Returns:
            response (str): The response from the Experience platform stating whether a batch succeeded or failed.
        """
        if not self.validate(datasetId):
            exit(0)
        batchId = self.ingestor.startBatch(datasetId, self.imsOrg, self.accessToken, self.apiKey)
        for fileName in files:
            if(os.path.getsize(fileName) <= MiB(256).to_Byte()):
                self.ingestor.upload(fileName, batchId, datasetId, self.imsOrg, self.accessToken, self.apiKey, self.cataloguer)
            else:
                self.ingestor.uploadLarge(fileName, batchId, datasetId, self.imsOrg, self.accessToken, self.apiKey, self.cataloguer)
        return self.ingestor.finishUpload(batchId, self.imsOrg, self.accessToken, self.apiKey, self.cataloguer)

    def error_checkJson(self, response):
        """
        A helper function which checks the given response object for errors and prints what those errors are.

        Args:
            response (Response): A Response object from the requests library.

        Returns:
            valid (bool): A boolean stating whether there was an error in the request or not.
        """
        if response.json().get('error'):
            print('Error: ' + response.json()['error_description'])
            return False
        if response.json().get('error_code'):
            print('Error: ' + response.json()['message'])
            return False
        if response.json().get('title'):
            if response.json()['title'] == "NotFoundError":
                print('Error: ' + response.json()['detail'])
                return False
        return True