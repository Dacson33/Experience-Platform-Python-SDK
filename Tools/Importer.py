from Interfaces.IngestorInterface import IngestorInterface
from Interfaces.CataloguerInterface import CataloguerInterface

class Importer:

    def __init__(self, ingestor:IngestorInterface, cataloguer:CataloguerInterface):
        self.ingestor = ingestor
        self.cataloguer = cataloguer

    def login(self):
        pass

    def upload(self):
        pass
