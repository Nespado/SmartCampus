import csv

from .file_adapter import FileAdapter
from .unified_data import UnifiedData


class CSVAdapter(FileAdapter):

    def __init__(self, fichier):
        self.fichier = fichier

    def adapt(self):

        donnees = []

        with open(
            self.fichier.path,
            "r",
            encoding="utf-8"
        ) as fichier_csv:

            lecteur = csv.DictReader(fichier_csv)

            for ligne in lecteur:
                donnees.append(dict(ligne))

        resultat = {
            "source": "CSV",
            "nom": self.fichier.name,
            "donnees": donnees
        }

        return UnifiedData(resultat)