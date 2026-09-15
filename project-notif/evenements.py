from abc import ABC
from datetime import date

class Salle:
    """Import Groupe 2 - Représente une salle du campus"""
    def __init__(self, nom: str):
        self.nom = nom

    def interagir(self, evenement: 'Evenement'):
        pass


class Evenement(ABC):
    """Classe abstraite représentant un événement sur le campus"""
    def __init__(self, date_evenement: date, description: str):
        self.date = date_evenement
        self.description = description


class Incendie(Evenement):
    def __init__(self, date_evenement: date, description: str, localisation: str):
        super().__init__(date_evenement, description)
        self.localisation = localisation


class CoursAnnule(Evenement):
    def __init__(self, date_evenement: date, description: str, nom_cours: str, raison: str):
        super().__init__(date_evenement, description)
        self.nomCours = nom_cours
        self.raison = raison


class AlerteConso(Evenement):
    def __init__(self, date_evenement: date, description: str, niveau: str, consommation: float):
        super().__init__(date_evenement, description)
        self.niveau = niveau
        self.consommation = consommation