from .reservation import Reservation


class ReservationSalle(Reservation):
    """Réservation concernant une salle."""

    def __init__(self, salle):
        self.salle = salle
        self.active = False

    def reserver(self):
        if self.active:
            print(f"{self.salle} est déjà réservée.")
            return

        self.active = True
        print(f"Réservation de {self.salle} effectuée.")

    def annuler(self):
        if not self.active:
            print(f"La réservation de {self.salle} est déjà annulée.")
            return

        self.active = False
        print(f"Réservation de {self.salle} annulée.")
