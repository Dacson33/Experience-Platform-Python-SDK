import requests
import time

from aep_sdk.Interfaces.CataloguerInterface import CataloguerInterface


class Cataloguer(CataloguerInterface):
    """
    An object that handles the reporting from the Adobe Experience Platform.

    Quick Methods:
        report(self, identification, ims_org, access_token, api_key):
            A function that checks and sends back the status of a batch.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for a Cataloguer object.
        """
        pass

    def report(self, identification, ims_org, access_token, api_key, full_response=False):
        """
        A function that checks and sends back the status of a batch.

        Args:
            identification (str): The id of the batch that is being checked.
            ims_org (str): The IMS Organization email of the user.
            access_token (AuthToken): The user's current active authorization token.
            api_key (str): The user's API Key for the Adobe Experience Platform.
            full_response (bool):  Whether or not to print the whole json response for querying a batch status.

        Returns:
            status (str): A string that is the status of the given batch.
        """

        headers = {
            'x-gw-ims-org-id': ims_org,
            'Authorization': 'Bearer ' + access_token.get_token(),
            'x-api-key': api_key
        }
        finished = False
        response = None
        while not finished:
            time.sleep(5)
            response = requests.get('https://platform.adobe.io/data/foundation/catalog/batches/' + identification,
                                    headers=headers)
            finished = False
            for idNum in response.json():
                if response.json()[idNum]['status'] == "loaded" or response.json()[idNum]['status'] == "loading"\
                        or response.json()[idNum]['status'] == "staging":
                    continue
                else:
                    finished = True
                    break
        for idNum in response.json():
            if full_response:
                print(response.json())
            print('Batch Status: ' + response.json()[idNum]['status'])
            return response.json()[idNum]['status']
