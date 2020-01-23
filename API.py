import requests
import json
import jwt
import datetime
import cryptography
import os
from bitmath import MiB

from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.DataSetId import DataSetId
from Tools.Cataloguer import Cataloguer
from Tools.Ingestor import Ingestor

class API:

    def __init__(self):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        self.apiKey = data['api_key']
        self.clientSecret = data['client_secret']
        self.dID = data['dataID']
        #Generation of the JWT token
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600),
            "iss": data['ims_org'],
            "sub": data['sub'],
            "https://ims-na1.adobelogin.com/s/ent_dataservices_sdk": True,
            "aud": 'https://ims-na1.adobelogin.com/c/' + data['api_key']
        }
        self.jwtToken = jwt.encode(payload, data['secret'], algorithm='RS256').decode('utf-8')
        self.imsOrg = data['ims_org']
        self.accessToken = self.access()
        self.datasetIds = self.dataId()
        self.cataloguer = Cataloguer()
        self.ingestor = Ingestor()
        #self.upload('Tests/test500.json', self.dID)

    #Sends a report of the status of the batch to the user
    def report(self, identification):
        self.cataloguer.report(identification, self.imsOrg, self.accessToken, self.apiKey)

    def validate(self, ids, dataSetID):
        realID = False
        for id in ids:
            if dataSetID == id.getIdentifier():
                realID = True
        return realID

    def send(self):
        pass

    #Generates the AuthToken for use with the API
    def access(self):
        files = {
            'client_id': (None, self.apiKey),
            'client_secret': (None, self.clientSecret),
            'jwt_token': (None, self.jwtToken),
        }
        testData = requests.post('https://ims-na1.adobelogin.com/ims/exchange/jwt/', files=files)
        #print(testData.json())
        if not self.error_checkJson(testData):
            exit(0)
        name = testData.json()['access_token']
        expiration = testData.json()['expires_in']
        authorization = AuthToken(name, expiration)
        return authorization

    def sandboxName(self):
        headers = {
            'Authorization': 'Bearer ' + self.accessToken.getToken(),
            'x-api-key': self.apiKey,
            'x-gw-ims-org-id': self.imsOrg,
        }
        params = (
            ('limit', '5'),
            ('properties', 'name'),
        )
        response = requests.get('https://platform.adobe.io/data/foundation/sandbox-management/sandboxes', headers=headers,
                                params=params)
        print('Sandbox')
        #print(response.json())
        #print(response.json()['name'])
        #return response.json()['name']
        return ""

    #Gets the datasetIDs tied to the user
    def dataId(self):
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
        #print(response.json())
        if not self.error_checkJson(response):
            exit(0)
        #In order to get a specific datasetID what we could do is iterate through the response and create multiple datasetID objects that way since we can access the key by index since response in an unordered dict
        for id in response.json():
            datasetID = DataSetId(id)
            ids.append(datasetID)
        realID = self.validate(ids, self.dID)
        if realID == False:
            print("The given datasetID is not found in the datasets tied to this account.")
            exit(0)
        return ids

    #Uploads the file to Experience Platform
    def upload(self, fileName, datasetId):
        if(os.path.getsize(fileName) <= MiB(256).to_Byte()):
            self.ingestor.upload(fileName, datasetId, self.imsOrg, self.accessToken, self.apiKey, self.cataloguer)
        else:
            self.ingestor.uploadLarge(fileName, datasetId, self.imsOrg, self.accessToken, self.apiKey, self.cataloguer)

    def error_checkJson(self, response):
        if response.json().get('error'):
            print('Error: ' + response.json()['error_description'])
            return False
        return True

#api = API()
#api.upload('Tests/test500.json', api.dID)