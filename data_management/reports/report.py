from datetime import date

from ..unified_data import UnifiedData


class Report:
    def __init__(self, titre: str, donnees: UnifiedData):
        self.titre = titre
        self.donnees = donnees
        self.date_creation = date.today()
        self.header = ""
        self.body = ""
