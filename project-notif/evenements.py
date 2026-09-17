from abc import ABC
from datetime import date


class Salle:
    """Import Groupe 2 - Représente une salle du campus"""

    def __init__(self, nom: str):
        self.nom = nom

    def interagir(self, evenement: 'CampusEvent'):
        pass


class CampusEvent(ABC):
    """Classe de base représentant un événement sur le campus (Groupe 1)."""

    def __init__(self, date_evenement: date, description: str):
        self.date = date_evenement
        self.date_evenement = date_evenement
        self.description = description


# Alias français pour compatibilité
Evenement = CampusEvent


class Incendie(CampusEvent):

    def __init__(self, date_evenement: date, description: str, localisation: str):
        super().__init__(date_evenement, description)
        self.localisation = localisation


class CoursAnnule(CampusEvent):

    def __init__(self, date_evenement: date, description: str, nom_cours: str, raison: str):
        super().__init__(date_evenement, description)
        self.nomCours = nom_cours
        self.nom_cours = nom_cours
        self.raison = raison


class AlerteConso(CampusEvent):

    def __init__(self, date_evenement: date, description: str, niveau: str, consommation: float):
        super().__init__(date_evenement, description)
        self.niveau = niveau
        self.consommation = consommation