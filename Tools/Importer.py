from Interfaces.IngestorInterface import IngestorInterface
from Interfaces.CataloguerInterface import CataloguerInterface
from Interfaces.ValidatorInterface import ValidatorInterface


class Importer:

    def __init__(self, ingestor:IngestorInterface, cataloguer:CataloguerInterface, validator:ValidatorInterface):
        self.ingestor = ingestor
        self.cataloguer = cataloguer
        self.validator = validator

    def login(self):
        pass

    def upload(self):
        pass
