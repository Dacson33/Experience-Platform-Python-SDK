from aep_sdk.Interfaces.CataloguerInterface import CataloguerInterface
import requests
import time


class Cataloguer(CataloguerInterface):
    """
    An object that handles the reporting from the Adobe Experience Platform.

    Quick Methods:
        report(self, identification, imsOrg, accessToken, apiKey):
            A function that checks and sends back the status of a batch.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for a Cataloguer object.
        """
        pass

    def report(self, identification, imsOrg, accessToken, apiKey):
        """
        A function that checks and sends back the status of a batch.

        Args:
            identification (str): The id of the batch that is being checked.
            imsOrg (str): The IMS Organization email of the user.
            accessToken (AuthToken): The user's current active authorization token.
            apiKey (str): The user's aep_sdk Key for the Adobe Experience Platform.

        Returns:
            status (str): A string that is the status of the given batch.
        """

        headers = {
            'x-gw-ims-org-id': imsOrg,
            'Authorization': 'Bearer ' + accessToken.getToken(),
            'x-api-key': apiKey
        }
        # response = requests.get('https://platform.adobe.io/data/foundation/catalog/batches/' + identification, headers=headers)
        # print(response.json())
        finished = False
        while not finished:
            time.sleep(5)
            response = requests.get('https://platform.adobe.io/data/foundation/catalog/batches/' + identification,
                                    headers=headers)
            finished = False
            for idNum in response.json():
                if response.json()[idNum]['status'] == "loaded" or response.json()[idNum]['status'] == "loading" or response.json()[idNum]['status'] == "staging":
                    continue
                else:
                    finished = True
                    break
        for idNum in response.json():
            print('Batch Status: ' + response.json()[idNum]['status'])
            return response.json()[idNum]['status']
