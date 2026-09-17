class Materiel:
    """Représente un matériel pouvant être réservé."""

    def __init__(self, identifiant, nom, disponible=True):
        self.id = identifiant
        self.nom = nom
        self.disponible = disponible

    def __str__(self):
        return f"{self.nom} ({self.id})"
