from smartcampus.reservations import ReservationSalle

from .fabrique_reservation import FabriqueReservation


class FabriqueReservationSalle(FabriqueReservation):
    """Crée une réservation pour une salle donnée."""

    def __init__(self, salle):
        self.salle = salle

    def creerReservation(self):
        return ReservationSalle(self.salle)
