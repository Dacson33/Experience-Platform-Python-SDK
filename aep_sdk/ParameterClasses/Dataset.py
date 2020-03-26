class Dataset:
    def __init__(self, identifier, name):
        self.id = identifier
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def __repr__(self):
        return "Name: " + str(self.name) + " - ID: " + str(self.id)

    def __str__(self):
        return "Name: " + str(self.name) + " - ID: " + str(self.id)
