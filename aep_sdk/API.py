import requests
import json
import jwt
import datetime
import os

from bitmath import MiB

from aep_sdk.ParameterClasses.AuthToken import AuthToken
from aep_sdk.ParameterClasses.Dataset import Dataset
from aep_sdk.Tools.Cataloguer import Cataloguer
from aep_sdk.Tools.Ingestor import Ingestor


class API:
    """
    The handler for the entire SDK.

    Attributes:
        access_token (AuthToken): The user's current active authorization token.
        api_key (str): The user's API Key for the Adobe Experience Platform.
        aud (str): The audience for the JWT token.
        cataloguer (Cataloguer): A Cataloguer object used for reporting.
        client_secret (str): The client_secret id of the user.
        ims_org (str): The IMS Organization email of the user.
        ingestor (Ingestor): An Ingestor object used for the handling of uploading files.
        jwt_token (str): The current JWT token.
        secret (str): The user's secret key used for the creation of JWT tokens.
        sub (str): The user's Technical Account id for Adobe I/O.

    Quick Methods:
        access(self):
            A function that generates and Auth Token for the current user.
        get_datasets(self):
            A function that queries and returns a list of datasets that are assigned to the current user.
        init_config(self, config_file):
            A function that initializes the config file and checks it for errors.
        report(self, identification):
            Runs the cataloguer report function, which will wait until the batch finishes loading before
             printing the batch status.
        upload(self, files, dataset_id, blocking):
            A function which uploads the given files to the given dataset ID using the ingestor.
        validate(self, data_set_id):
            A function that checks if a given dataset ID exists for the current account.
    """

    def __init__(self, config_file):
        """
        Constructs all the necessary attributes for an API object.

        Args:
            config_file (str): The full name and path of the config file.
        """
        self.api_key = None
        self.client_secret = None
        self.ims_org = None
        self.sub = None
        self.secret = None
        self.aud = None

        if not self.init_config(config_file):
            print("Bad config file")
            exit(0)

        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600),
            "iss": self.ims_org,
            "sub": self.sub,
            "https://ims-na1.adobelogin.com/s/ent_dataservices_sdk": True,
            "aud": self.aud
        }
        self.jwt_token = jwt.encode(payload, self.secret, algorithm='RS256').decode('utf-8')
        self.access_token = self.access()
        self.cataloguer = Cataloguer()
        self.ingestor = Ingestor()
        
    def init_config(self, config_file):
        """
        A function that initializes the config file and checks it for errors.

        Args:
            config_file (str): The full name and path of the config file.

        Returns:
            initialized (bool): A boolean stating if the config was successfully initialized or not.
        """

        with open(config_file) as json_data_file:
            data = json.load(json_data_file)
        if not data.get('api_key'):
            return False
        self.api_key = data['api_key']
        if not self.validate_string(self.api_key):
            return False
        if not data.get('client_secret'):
            return False
        self.client_secret = data['client_secret']
        if not self.validate_string(self.client_secret):
            return False
        if not data.get('ims_org'):
            return False
        self.ims_org = data['ims_org']
        if not self.validate_string(self.ims_org):
            return False
        if not data.get('sub'):
            return False
        self.sub = data['sub']
        if not self.validate_string(self.sub):
            return False
        if not data.get('secret'):
            return False
        self.secret = data['secret']
        if not self.validate_string(self.secret):
            return False
        self.aud = 'https://ims-na1.adobelogin.com/c/' + self.api_key
        return True

    def validate_string(self, obj):
        """
        A helper function that checks if an object from the config json file is not null or the empty string.

        Args:
            obj (str): The string we are validating.

        Returns:
            valid (bool): A boolean stating if the object was null/empty or not.
        """
        if obj is None or obj == "":
            return False
        return True

    def report(self, identification, full_response=False):
        """
        Runs the cataloguer report function, which will wait until the batch finishes loading before printing
         the batch status.

        Args:
            identification (str): The dataset ID of the batch to report on.
            full_response (bool): Whether or not to print the whole json response for querying a batch status.
        """
        self.cataloguer.report(identification, self.ims_org, self.access_token, self.api_key, full_response)

    def validate(self, data_set_id):
        """
        A function that checks if a given dataset ID exists for the current account.

        Args:
            data_set_id (str): A dataset ID to validate.

        Returns:
            exists (bool): A boolean stating whether the dataset ID exists on the current account.
        """
        if data_set_id == "":
            print("You need to enter a DataSetID.")
            return False
        headers = {
            'Authorization': 'Bearer ' + self.access_token.get_token(),
            'x-api-key': self.api_key,
            'x-gw-ims-org-id': self.ims_org,
        }
        params = (
            ('properties', 'name,description,state,tags,files'),
        )
        response = requests.get('https://platform.adobe.io/data/foundation/catalog/dataSets/' + data_set_id,
                                headers=headers, params=params)
        if not self.error_check_json(response):
            return False
        return True

    def access(self):
        """
        A function that generates an Auth Token for the current user.

        Returns:
            authorization (AuthToken): An valid authorization token for the current user that will last for 24 hours.
        """
        files = {
            'client_id': (None, self.api_key),
            'client_secret': (None, self.client_secret),
            'jwt_token': (None, self.jwt_token),
        }
        test_data = requests.post('https://ims-na1.adobelogin.com/ims/exchange/jwt/', files=files)
        if not self.error_check_json(test_data):
            exit(0)
        name = test_data.json()['access_token']
        expiration = test_data.json()['expires_in']
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(milliseconds=expiration - 1000)
        authorization = AuthToken(name, expiration, expiration_date)
        return authorization

    def get_datasets(self, limit=5):
        """
        A function that queries and returns a list of datasets that are assigned to the current user.

        Returns:
            datasets (list): A list of datasets belonging to the current account.
        """
        headers = {
            'Authorization': 'Bearer ' + self.access_token.get_token(),
            'x-api-key': self.api_key,
            'x-gw-ims-org-id': self.ims_org,
        }
        params = (
            ('limit', limit),
            ('properties', 'name'),
        )
        response = requests.get('https://platform.adobe.io/data/foundation/catalog/dataSets',
                                headers=headers, params=params)
        ids = []
        if not self.error_check_json(response):
            exit(0)
        for response_id in response.json():
            ids.append(Dataset(response_id, response.json()[response_id]['name']))
        return ids

    def upload(self, files, dataset_id, blocking=True):
        """
        A function which uploads the given json files to the given dataset ID using the ingestor.

        Args:
            files (list): A list of strings which are the full path and names of the files being uploaded.
            dataset_id (str): The dataset ID that is being uploaded to.
            blocking (bool): Whether or not to block and wait for a report of the upload success or failure.

        Returns:
            response (str): The response from the Experience platform stating whether a batch succeeded or failed.
        """
        if not self.validate(dataset_id):
            exit(0)
        batch_id = self.ingestor.start_batch(dataset_id, self.ims_org, self.access_token, self.api_key)
        for fileName in files:
            if os.path.getsize(fileName) <= MiB(256).to_Byte():
                self.ingestor.upload(fileName, batch_id, dataset_id, self.ims_org, self.access_token, self.api_key)
            else:
                self.ingestor.upload_large(fileName, batch_id, dataset_id, self.ims_org,
                                           self.access_token, self.api_key)
        return self.ingestor.finish_upload(batch_id, self.ims_org, self.access_token, self.api_key,
                                           self.cataloguer, blocking)

    def error_check_json(self, response):
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
