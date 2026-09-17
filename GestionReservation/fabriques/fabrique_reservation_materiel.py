from smartcampus.reservations import ReservationMateriel

from .fabrique_reservation import FabriqueReservation


class FabriqueReservationMateriel(FabriqueReservation):
    """Crée une réservation pour un matériel donné."""

    def __init__(self, materiel):
        self.materiel = materiel

    def creerReservation(self):
        return ReservationMateriel(self.materiel)
