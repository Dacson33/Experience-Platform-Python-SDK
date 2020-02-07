import requests
import json
import jwt
import datetime
import cryptography
import os
from bitmath import MiB
import time

from ParameterClasses.AuthToken import AuthToken
from ParameterClasses.DataSetId import DataSetId
from Tools.Cataloguer import Cataloguer
from Tools.Ingestor import Ingestor

class API:

    def __init__(self, configFile):
        if not self.initConfig(configFile):
            print("Bad config file")
            exit(0)
        #Generation of the JWT token
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600),
            "iss": self.imsOrg,
            "sub": self.sub,
            "https://ims-na1.adobelogin.com/s/ent_dataservices_sdk": True,
            "aud": self.aud
        }
        self.jwtToken = jwt.encode(payload, self.secret, algorithm='RS256').decode('utf-8')
        #self.imsOrg = data['ims_org']
        self.accessToken = self.access()
        #self.accessToken = AuthToken("eyJ4NXUiOiJpbXNfbmExLWtleS0xLmNlciIsImFsZyI6IlJTMjU2In0.eyJpZCI6IjE1ODA3NTU5MzM0OTFfNTM3ZDZiYWQtNmJjOS00YWFjLWEwZTktMDEzM2YyOTFiNzYxX3VlMSIsImNsaWVudF9pZCI6ImQ4YjY1Y2E3NWVlNDRiOGNhOWJmODdiNmZkYzBhMTc0IiwidXNlcl9pZCI6IkQ5Q0I3OEEyNURBRTE0QkMwQTQ5NUMyMUB0ZWNoYWNjdC5hZG9iZS5jb20iLCJzdGF0ZSI6IntcInNlc3Npb25cIjpcImh0dHBzOi8vaW1zLW5hMS5hZG9iZWxvZ2luLmNvbS9pbXMvc2Vzc2lvbi92MS9aakExT1daak1Ea3RabU5tWmkwME1qTTFMV0V5WkRRdFlqUmlNREV3TnpOalpXTTBMUzFFT1VOQ056aEJNalZFUVVVeE5FSkRNRUUwT1RWRE1qRkFkR1ZqYUdGalkzUXVZV1J2WW1VdVkyOXRcIn0iLCJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiYXMiOiJpbXMtbmExIiwiZmciOiJVRkFLWUpFMkhQRTVKUFVQRzZBTFlQUUFEVT09PT09PSIsIm1vaSI6IjU0YmVlZjg3IiwiYyI6IlRrZnhXK3dwRStzZk9TbGc1RlZITlE9PSIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsInNjb3BlIjoib3BlbmlkLHNlc3Npb24sQWRvYmVJRCxyZWFkX29yZ2FuaXphdGlvbnMsYWRkaXRpb25hbF9pbmZvLnByb2plY3RlZFByb2R1Y3RDb250ZXh0IiwiY3JlYXRlZF9hdCI6IjE1ODA3NTU5MzM0OTEifQ.psJCN3iFkzMx9bgkQBB4cDBHzvuHK6eLT146iw1z-89kf0m0iPqshJuX3ddToUWp3hXEbZWkr9Ta1BezbjTvSnpgtYbNFAs4M2mYnVHpzqCgJQxI41JzQKHAqj94_dHNJIWvHJERnME1L9dX0DHSmFSTSZVwOUZWT7HFdZg-2wPTG4wY3VRVmiwVmmW3lQAJ5aL6N7O1rWUqEEb9tXHM9UJSKeFTdlsmyAX_MV9TK9-zB5kDpkhMK41rQiwUVWzCkB1gawJPutweGv5GiUieOOlwLz0GfD5oH5aoA8FYXt9_hFziQPP55yVoxbYWuOPFMiqRBWmL_zbne8D4Kn7Uwg", "07907987979", "0")
        if not self.validate(self.dID):
            exit(0)
        self.cataloguer = Cataloguer()
        self.ingestor = Ingestor()
        #self.upload('Tests/test500.json', self.dID)

    def initConfig(self, configFile):
        with open(configFile) as json_data_file:
            data = json.load(json_data_file)
        if not data.get('api_key'):
            return False
        self.apiKey = data['api_key']
        if not self.checkNull(self.apiKey):
            return False
        if not data.get('client_secret'):
            return False
        self.clientSecret = data['client_secret']
        if not self.checkNull(self.clientSecret):
            return False
        if not data.get('dataID'):
            return False
        self.dID = data['dataID']
        if not self.checkNull(self.dID):
            return False
        if not data.get('ims_org'):
            return False
        self.imsOrg = data['ims_org']
        if not self.checkNull(self.imsOrg):
            return False
        if not data.get('sub'):
            return False
        self.sub = data['sub']
        if not self.checkNull(self.sub):
            return False
        if not data.get('secret'):
            return False
        self.secret = data['secret']
        if not self.checkNull(self.secret):
            return False
        self.aud = 'https://ims-na1.adobelogin.com/c/' + self.apiKey
        return True

    def checkNull(self, obj):
        if obj == None or obj == "":
            return False
        return True

    #Sends a report of the status of the batch to the user
    def report(self, identification):
        self.cataloguer.report(identification, self.imsOrg, self.accessToken, self.apiKey)

    def validate(self, dataSetID):
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
        #print(response.json())
        if not self.error_checkJson(response):
            #print("The given datasetID is not found in the datasets tied to this account.")
            return False
        return True


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
        expirationDate = datetime.datetime.utcnow() + datetime.timedelta(milliseconds=expiration - 1000)
        authorization = AuthToken(name, expiration, expirationDate)
        #print(authorization.getToken())
        #print(authorization.getExpiration())
        #print(authorization.getExpirationDate())
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
            #print(id)
            datasetID = DataSetId(id)
            ids.append(datasetID)
        realID = True
        if realID == False:
            print("The given datasetID is not found in the datasets tied to this account.")
            exit(0)
        return ids

    #Uploads the file to Experience Platform
    def upload(self, fileName, datasetId):
        if(os.path.getsize(fileName) <= MiB(256).to_Byte()):
            return self.ingestor.upload(fileName, datasetId, self.imsOrg, self.accessToken, self.apiKey, self.cataloguer)
        else:
            return self.ingestor.uploadLarge(fileName, datasetId, self.imsOrg, self.accessToken, self.apiKey, self.cataloguer)

    def error_checkJson(self, response):
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

#api = API('config.json')
#print(api.validate(""))
#batch = api.upload('Tests/test256.json', api.dID)
#time.sleep(20)
#api.cataloguer.report(batch, api.imsOrg, api.accessToken, api.apiKey)
#api.ingestor.new_split('Tests/test500.json')
