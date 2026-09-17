class Salle:
    """Représente une salle du campus."""

    def __init__(self, identifiant, nom):
        self.id = identifiant
        self.nom = nom

    def __str__(self):
        return f"Salle {self.nom} ({self.id})"
