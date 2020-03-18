import requests
import os
import json
import csv

from _csv import QUOTE_ALL
from bitmath import MiB

from Interfaces.IngestorInterface import IngestorInterface
from ParameterClasses.AuthToken import AuthToken


class Ingestor(IngestorInterface):
    """
    An object that handles the uploading of files to the Adobe Experience Platform.

    Quick Methods:
        error_check(self, response):
            A function that checks if a response object was valid.
        finish_upload(self, batch_id, ims_org, access_token: AuthToken, api_key, cataloguer, blocking):
            A function that signals the completion of the batch.
        new_split(self, file_name):
            A function that splits up JSON files of sizes greater than 256MB.
        send_file(self, file_name, batch_id, dataset_id, ims_org, access_token: AuthToken, api_key):
            A function that sends the file to a batch to be uploaded.
        start_batch(self, dataset_id, ims_org, access_token: AuthToken, api_key):
            A function that creates the batch that the files will upload to.
        upload(self, file_name, batch_id, dataset_id, ims_org, access_token:AuthToken, api_key):
            A function that handles the uploading of files of sizes less than or equal to 256MB.
        upload_large(self, file_name, batch_id, dataset_id, ims_org, access_token:AuthToken, api_key):
            A function that handles the uploading of files of sizes greater than 256MB.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for an Ingestor object.
        """
        self.current_index = 0
        pass

    def start_batch(self, dataset_id, ims_org, access_token: AuthToken, api_key):
        """
        A function that creates the batch that the files will upload to.

        Args:
            dataset_id (str): The string that is the dataset ID that is being uploaded to.
            ims_org (str): The IMS Organization email of the user.
            access_token (AuthToken): The user's current active authorization token.
            api_key (str): The user's API Key for the Adobe Experience Platform.

        Returns:
            batch_id (str): A string that is the id of the batch that has just been created.
        """

        headers = {
            'Content-Type': 'application/json',
            'x-gw-ims-org-id': ims_org,
            'Authorization': 'Bearer ' + access_token.get_token(),
            'x-api-key': api_key
        }
        data = '{\n          "datasetId": "'\
               + dataset_id\
               + '",\n           "inputFormat": {\n' \
               + '                "format": "json",\n' \
               + '                "isMultiLineJson": true\n           }\n      }'
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches', headers=headers, data=data)
        print('Create batch status: ' + response.json()['status'])
        batch_id = response.json()['id']
        print(batch_id)
        return batch_id

    def send_file(self, file_name, batch_id, dataset_id, ims_org, access_token: AuthToken, api_key):
        """
        A function that sends the file to a batch to be uploaded.

        Args:
            file_name (str): The full name and path of the file to be uploaded.
            batch_id (str): The id of the batch that the file is being sent to.
            dataset_id (str): The id of the dataset that is being uploaded to.
            ims_org (str): The IMS Organization email of the user.
            access_token (AuthToken): The user's current active authorization token.
            api_key (str): The user's API Key for the Adobe Experience Platform.

        Returns:
            response (Response): The response object given by the put request to the Adobe Experience Platform.
        """

        headers = {
            'Content-Type': 'application/octet-stream',
            'x-gw-ims-org-id': ims_org,
            'Authorization': 'Bearer ' + access_token.get_token(),
            'x-api-key': api_key
        }
        print('File upload of ' + os.path.basename(file_name) + ' in progress')
        file = open(file_name, 'rb')
        data = file.read()
        file.close()
        response = requests.put('https://platform.adobe.io/data/foundation/import/batches/' + batch_id + '/datasets/'
                                + dataset_id + '/files/' + os.path.basename(file_name), headers=headers, data=data)
        return response

    def finish_upload(self, batch_id, ims_org, access_token: AuthToken, api_key, cataloguer, blocking=True):
        """
        A function that signals the completion of the batch.

        Args:
            batch_id (str): The id of the batch currently being uploaded.
            ims_org (str): The IMS Organization email of the user.
            access_token (AuthToken): The user's current active authorization token.
            api_key (str): The user's API Key for the Adobe Experience Platform.
            cataloguer (Cataloguer): A Cataloguer object used for reporting the batch status.
            blocking (bool): Whether or not to block and wait for a report of the upload success or failure.

        Returns:
            status (str): The string of the batch status given by the cataloguer's report function.
        """

        headers = {
            'x-gw-ims-org-id': ims_org,
            'Authorization': 'Bearer ' + access_token.get_token(),
            'x-api-key': api_key
        }
        params = (
            ('action', 'COMPLETE'),
        )
        print('Signal Completion: ')
        response = requests.post('https://platform.adobe.io/data/foundation/import/batches/' + batch_id,
                                 headers=headers, params=params)
        if not self.error_check(response):
            print("Signal Completion has failed for " + batch_id)
        else:
            print(batch_id + " upload started successfully")
        if blocking:
            return cataloguer.report(batch_id, ims_org, access_token, api_key)
        else:
            return "Your Upload is in Progress"

    def upload(self, file_name, batch_id, dataset_id, ims_org, access_token: AuthToken, api_key):
        """
        A function that handles the uploading of files of sizes less than or equal to 256MB.

        Args:
            file_name (str): The full name and path of the file being uploaded.
            batch_id (str): The id of the batch that is being used.
            dataset_id (str): The id of the dataset that is being uploaded to.
            ims_org (str): The IMS Organization email of the user.
            access_token (AuthToken): The user's current active authorization token.
            api_key (str): The user's API Key for the Adobe Experience Platform.
        """
        if file_name.lower().endswith(".csv"):
            self.csv_split(file_name, ',')
            for entry in os.scandir('Splits/'):
                response = self.send_file(entry.path, batch_id, dataset_id, ims_org, access_token, api_key)
                if not self.error_check(response):
                    print(os.path.basename(entry.path) + ' failed to upload')
                    continue
                os.remove(entry.path)
            os.rmdir('Splits/')
        elif file_name.lower().endswith(".tsv"):
            self.csv_split(file_name, '\t')
            for entry in os.scandir('Splits/'):
                response = self.send_file(entry.path, batch_id, dataset_id, ims_org, access_token, api_key)
                if not self.error_check(response):
                    print(os.path.basename(entry.path) + ' failed to upload')
                    continue
                os.remove(entry.path)
            os.rmdir('Splits/')
        else:
            response = self.send_file(file_name, batch_id, dataset_id, ims_org, access_token, api_key)
            if not self.error_check(response):
                return

    def upload_large(self, file_name, batch_id, dataset_id, ims_org, access_token: AuthToken, api_key):
        """
        A function that handles the uploading of files of sizes greater than 256MB.

        Args:
            file_name (str): The full name and path of the file being uploaded.
            batch_id (str): The id of the batch that is being used.
            dataset_id (str): The id of the dataset that is being uploaded to.
            ims_org (str): The IMS Organization email of the user.
            access_token (AuthToken): The user's current active authorization token.
            api_key (str): The user's API Key for the Adobe Experience Platform.
        """
        if file_name.lower().endswith(".json"):
            self.json_split(file_name)
        elif file_name.lower().endswith(".csv"):
            self.csv_split(file_name, ',')
        elif file_name.lower().endswith(".tsv"):
            self.csv_split(file_name, '\t')
        for entry in os.scandir('Splits/'):
            response = self.send_file(entry.path, batch_id, dataset_id, ims_org, access_token, api_key)
            if not self.error_check(response):
                print(os.path.basename(entry.path) + ' failed to upload')
                continue
            os.remove(entry.path)
        os.rmdir('Splits/')

    def error_check(self, response):
        """
        A function that checks if a response object was valid.

        Args:
            response (Response): A response object from the requests library.

        Returns:
            valid (bool): A boolean stating whether there was an error code or not.
        """
        if response.status_code != 200:
            print("Error: " + response.status_code)
            return False
        return True

    def _one_pass(self, iterators):
        """
        Helper for the new_split function.
        """
        i = 0
        while i < len(iterators):
            try:
                yield next(iterators[i])
            except StopIteration:
                del iterators[i]
            else:
                i += 1

    def zip_var_len(self, *iterables):
        """
        Helper for the new_split function.
        """
        iterators = [iter(it) for it in iterables]
        while True:
            val = tuple(self._one_pass(iterators))
            if val:
                yield val
            else:
                break

    def grouper(self, iterable, n):
        """
        Helper for the new_split function.
        """
        "Collect data into fixed-length chunks or blocks"
        args = [iter(iterable)] * n
        return self.zip_var_len(*args)

    def json_split(self, file_name):
        """
        A function that splits up JSON files of sizes greater than 256MB.

        Args:
            file_name: The full name and path of the file being split.
        """
        file = open(file_name, 'rb')
        values = file.read()
        file.close()
        v = json.loads(values)
        os.mkdir('Splits/')
        for i, group in enumerate(self.grouper(v, 125000)):
            self.current_index = self.current_index + 1
            with open('Splits/' + os.path.splitext(os.path.basename(file_name))[0]
                      + '_{}.json'.format(self.current_index), 'w') as output_file:
                json.dump(list(group), output_file)

    def csv_split_old(self, file_name, delimiter):
        first_line = ""
        output_text = []
        first = True
        row_length = 0
        first_row_length = 0
        os.mkdir('Splits/')
        with open(file_name, 'r') as f:
            reader = csv.reader(f, delimiter=delimiter, quoting=QUOTE_ALL)
            i = 0
            for row in reader:
                if first:
                    row_length = self.utf8len(delimiter.join(row)) + 6
                    print(row_length)
                    first_row_length = row_length
                    first_line = row
                    first = False
                    continue
                row_length = row_length + self.utf8len(delimiter.join(row)) + 6
                print(row_length)
                output_text.append(row)
                if row_length > MiB(256).to_Byte():
                    self.write_to_csv(file_name, output_text, first_line, i, delimiter)
                    i = i + 1
                    output_text = []
                    row_length = first_row_length
            if output_text is not []:
                self.write_to_csv(file_name, output_text, first_line, i, delimiter)
        return

    def write_to_csv(self, file_name, output_text, headers, index, delimiter):
        extension = '.csv'
        if delimiter == '\t':
            extension = '.tsv'
        if delimiter == ',':
            extension = '.csv'
        with open('Splits/' + os.path.splitext(os.path.basename(file_name))[0]
                  + '_{}'.format(index) + extension, 'w') as output_file:
            writer = csv.writer(output_file, delimiter=delimiter, lineterminator='\n')
            writer.writerow(headers)
            writer.writerows(output_text)

    def utf8len(self, s):
        return len(s.encode('utf-8'))

    def csv_split(self, file_name, delimiter):
        os.mkdir('Splits/')
        with open('Splits/' + os.path.splitext(os.path.basename(file_name))[0]
                  + '_{}.json'.format(self.current_index), 'w') as json_file:
            with open(file_name, 'r') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=delimiter)
                out = json.dumps([row for row in reader])
                json_file.write(out)
