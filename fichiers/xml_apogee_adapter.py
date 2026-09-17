import xml.etree.ElementTree as ET

from .file_adapter import FileAdapter
from .unified_data import UnifiedData


class XmlApogeeAdapter(FileAdapter):

    def __init__(self, fichier):
        self.fichier = fichier

    def adapt(self):

        arbre = ET.parse(self.fichier.path)
        racine = arbre.getroot()

        donnees = []

        for element in racine:

            ligne = {}

            for enfant in element:
                ligne[enfant.tag] = enfant.text

            donnees.append(ligne)

        resultat = {
            "source": "XML APOGEE",
            "nom": self.fichier.name,
            "donnees": donnees
        }

        return UnifiedData(resultat)