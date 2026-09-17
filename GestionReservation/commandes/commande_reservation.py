from .commande import Commande


class CommandeReservation(Commande):
    """Commande qui réserve une salle ou un matériel."""

    def __init__(self, reservation):
        self.reservation = reservation

    def executer(self):
        self.reservation.reserver()

    def defaire(self):
        self.reservation.annuler()
