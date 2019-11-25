import requests
import json

from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.DataSetId import DataSetId


class API:

    def __init__(self):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        self.apiKey = data['api_key']
        self.clientSecret = data['client_secret']
        self.jwtToken = data['jwt_token']
        self.imsOrg = data['ims_org']
        self.accessToken = self.access()
        self.sandbox = self.sandboxName()
        self.datasetId = self.dataId()

    def report(self):
        pass

    def validate(self):
        pass

    def send(self):
        pass

    def access(self):
        print(self.apiKey)
        print(self.clientSecret)
        print(self.jwtToken)
        files = {
            'client_id': (None, self.apiKey),
            'client_secret': (None, self.clientSecret),
            'jwt_token': (None, self.jwtToken),
        }
        testData = requests.post('https://ims-na1.adobelogin.com/ims/exchange/jwt/', files=files)
        print(testData.json())
        #name = testData.json()['access_token']
        #expiration = testData.json()['expires_in']
        #authorization = AuthToken(name, expiration)
        #return authorization
        return ""

    def sandboxName(self):
        print(self.apiKey)
        print(self.clientSecret)
        print(self.jwtToken)
        print(self.accessToken)
        headers = {
            'Authorization': 'Bearer ' + self.accessToken,
            'x-api-key': self.apiKey,
            'x-gw-ims-org-id': self.imsOrg,
        }
        params = (
            ('limit', '5'),
            ('properties', 'name'),
        )
        response = requests.get('https://platform.adobe.io/data/foundation/sandbox-management/sandboxes', headers=headers,
                                params=params)
        print(response.json())
        #return response.json()['name']
        return ""

    def dataId(self):
        print(self.apiKey)
        print(self.clientSecret)
        print(self.jwtToken)
        print(self.accessToken)
        headers = {
            'Authorization': 'Bearer ' + self.accessToken,
            'x-api-key': self.apiKey,
            'x-gw-ims-org-id': self.imsOrg,
            'x-sandbox-name': '{SANDBOX_NAME}',
        }
        params = (
            ('limit', '5'),
            ('properties', 'name'),
        )
        response = requests.get('https://platform.adobe.io/data/foundation/catalog/dataSets', headers=headers, params=params)
        print(response.json())
        #datasetID = DataSetId(response.json())
        return response.json()

    def upload(self, fileName):
        headers = {
            'content-type': 'application/octet-stream',
            'x-gw-ims-org-id': self.imsOrg,
            'x-sandbox-name': self.sandbox,
            'Authorization': 'Bearer ' + self.accessToken,
            'x-api-key': self.apiKey,
        }
        data = {
            'datasetId': self.datasetId
        }
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches', headers=headers, data=data)
        batchId = response.json()['id']
        data = open('Tests/' + fileName, 'rb').read()
        response = requests.put('https://platform.adobe.io/data/foundation/import/batches/' + batchId + '/datasets/' + self.datasetId + '/files/' + fileName, headers=headers, data=data)
        return response.json()


api = API()
