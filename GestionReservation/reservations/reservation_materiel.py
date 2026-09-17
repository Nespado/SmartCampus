from .reservation import Reservation


class ReservationMateriel(Reservation):
    """Réservation concernant un matériel."""

    def __init__(self, materiel):
        self.materiel = materiel
        self.active = False

    def reserver(self):
        if self.active:
            print(f"{self.materiel} est déjà réservé.")
            return

        if not self.materiel.disponible:
            raise ValueError(f"{self.materiel} n'est pas disponible.")

        self.active = True
        self.materiel.disponible = False
        print(f"Réservation du matériel {self.materiel} effectuée.")

    def annuler(self):
        if not self.active:
            print(f"La réservation de {self.materiel} est déjà annulée.")
            return

        self.active = False
        self.materiel.disponible = True
        print(f"Réservation du matériel {self.materiel} annulée.")
