from Interfaces.CataloguerInterface import CataloguerInterface
import requests


class Cataloguer(CataloguerInterface):

    def __init__(self):
        pass

    def report(self, identification, imsOrg, accessToken, apiKey):
        headers = {
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        response = requests.get('https://platform.adobe.io/data/foundation/catalog/batches/' + identification, headers=headers)
        print(response.json())
        for idNum in response.json():
            print('Batch Status: ' + response.json()[idNum]['status'])
