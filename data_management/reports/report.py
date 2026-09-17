from datetime import date

class Report:
    def __init__(self, titre, donnees):
        self.titre = titre
        self.donnees = donnees
        self.date_creation = date.today()