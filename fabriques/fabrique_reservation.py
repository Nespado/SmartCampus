from abc import ABC, abstractmethod


class FabriqueReservation(ABC):
    """Fabrique abstraite de réservations."""

    @abstractmethod
    def creerReservation(self):
        pass
