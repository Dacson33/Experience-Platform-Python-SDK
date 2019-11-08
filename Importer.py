from ToolsInterfaces.IngestorInterface import IngestorInterface
from ToolsInterfaces.CataloguerInterface import CataloguerInterface


class Importer:

    def __init__(self, ingestor, cataloguer):
        self.ingestor = ingestor
        self.cataloguer = cataloguer

    def login(self):
        pass

    def upload(self):
        pass
