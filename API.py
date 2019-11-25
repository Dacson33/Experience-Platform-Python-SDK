import requests
import json

class API:

    def __init__(self):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        self.apiKey = data['api_key']
        self.clientSecret = data['client_secret']
        self.jwtToken = data['jwt_token']
        self.imsOrg = data['ims_org']
        self.access = ''
  
    def report(self):
        pass
  
    def validate(self):
        pass
  
    def send(self):
        pass
  
    def upload(self):
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
        self.access = testData.json()['access_token']

api = API()
api.upload()
