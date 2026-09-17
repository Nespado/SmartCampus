from .commande import Commande


class CommandeAnnulation(Commande):
    """Commande qui annule une réservation."""

    def __init__(self, reservation):
        self.reservation = reservation

    def executer(self):
        self.reservation.annuler()

    def defaire(self):
        self.reservation.reserver()
