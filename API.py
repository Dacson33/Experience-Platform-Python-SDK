import requests
import json
import jwt
import datetime
import cryptography

from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.DataSetId import DataSetId


class API:

    def __init__(self):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        self.apiKey = data['api_key']
        self.clientSecret = data['client_secret']
        self.dID = data['dataID']
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600),
            "iss": data['ims_org'],
            "sub": data['sub'],
            "https://ims-na1.adobelogin.com/s/ent_dataservices_sdk": True,
            "aud": 'https://ims-na1.adobelogin.com/c/' + data['api_key']
        }
        #print(payload['aud'])
        #self.jwtToken = data['jwt_token']
        self.jwtToken = jwt.encode(payload, data['secret'], algorithm='RS256').decode('utf-8')
        #print(self.jwtToken)
        self.imsOrg = data['ims_org']
        self.accessToken = self.access()
        #self.sandbox = self.sandboxName()
        self.datasetIds = self.dataId()
        self.upload('test128.json', self.dID)

    def report(self, identification):
        headers = {
            'x-gw-ims-org-id': self.imsOrg,
            'Authorization': 'Bearer ' + self.accessToken.getToken(),
            'x-api-key': self.apiKey
        }

        response = requests.get('https://platform.adobe.io/data/foundation/catalog/batches/' + identification, headers=headers)
        for id in response.json():
            print('Batch Status: ' + response.json()[id]['status'])

    def validate(self):
        pass

    def send(self):
        pass

    def access(self):
        files = {
            'client_id': (None, self.apiKey),
            'client_secret': (None, self.clientSecret),
            'jwt_token': (None, self.jwtToken),
        }
        testData = requests.post('https://ims-na1.adobelogin.com/ims/exchange/jwt/', files=files)
        #print('Access')
        #print(testData.json())
        name = testData.json()['access_token']
        #print(name)
        expiration = testData.json()['expires_in']
        #print(expiration)
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

    def dataId(self):
        headers = {
            'Authorization': 'Bearer ' + self.accessToken.getToken(),
            'x-api-key': self.apiKey,
            'x-gw-ims-org-id': self.imsOrg,
            #'x-sandbox-name': self.sandbox,
        }
        params = (
            ('limit', '5'),
            ('properties', 'name'),
        )
        response = requests.get('https://platform.adobe.io/data/foundation/catalog/dataSets', headers=headers, params=params)
        #print('DataSetID')
        #print('  ' + response.json())
        ids = []
        #In order to get a specific datasetID what we could do is iterate through the response and create multiple datasetID objects that way since we can access the key by index since response in an unordered dict
        for id in response.json():
            datasetID = DataSetId(id)
            ids.append(datasetID)
        #datasetID = DataSetId(response.json())
        return ids

    def upload(self, fileName, datasetId):
        headers = {
            'Content-Type': 'application/json',
            'x-gw-ims-org-id': self.imsOrg,
            'Authorization': 'Bearer ' + self.accessToken.getToken(),
            'x-api-key': self.apiKey
        }
        data = '{ \n          "datasetId": "'+datasetId+'" \n      }'
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches', headers=headers, data=data)
        print('Create batch status: ' + response.json()['status'])
        batchId = response.json()['id']
        headers = {
            'Content-Type': 'application/octet-stream',
            'x-gw-ims-org-id': self.imsOrg,
            'Authorization': 'Bearer ' + self.accessToken.getToken(),
            'x-api-key': self.apiKey
        }

        print('File upload of ' + fileName + ' in progress')
        data = open('Tests/' + fileName, 'rb').read()
        response = requests.put('https://platform.adobe.io/data/foundation/import/batches/' + batchId + '/datasets/' + datasetId + '/files/' + fileName, headers=headers, data=data)
        print(response)
        headers = {
            'x-gw-ims-org-id': self.imsOrg,
            'Authorization': 'Bearer ' + self.accessToken.getToken(),
            'x-api-key': self.apiKey
        }
        params = (
            ('action', 'COMPLETE'),
        )
        print('Signal Completion: ')
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches/' + batchId, headers=headers, params=params)
        print(response)
        self.report(batchId)

api = API()