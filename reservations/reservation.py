from abc import ABC, abstractmethod


class Reservation(ABC):
    """Interface commune à toutes les réservations."""

    @abstractmethod
    def reserver(self):
        pass

    @abstractmethod
    def annuler(self):
        pass
