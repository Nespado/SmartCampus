class LegacyFile:

    def __init__(self, name, path, type):
        self.name = name
        self.path = path
        self.type = type

    def afficher_info(self):
        print(f"Nom : {self.name}")
        print(f"Chemin : {self.path}")
        print(f"Type : {self.type}")