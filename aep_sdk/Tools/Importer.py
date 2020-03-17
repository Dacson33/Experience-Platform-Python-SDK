from aep_sdk.Interfaces import IngestorInterface
from aep_sdk.Interfaces.CataloguerInterface import CataloguerInterface
from aep_sdk.Interfaces import ValidatorInterface


class Importer:

    def __init__(self, ingestor:IngestorInterface, cataloguer:CataloguerInterface, validator:ValidatorInterface):
        self.ingestor = ingestor
        self.cataloguer = cataloguer
        self.validator = validator

    def login(self):
        pass

    def upload(self):
        pass
