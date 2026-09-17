from smartcampus.commandes import (
    CommandeAnnulation,
    CommandeReservation,
    GestionnaireCommandes,
)


class ServiceReservation:
    """Point d'entrée pour réserver et gérer l'historique des actions."""

    def __init__(self, fabrique):
        self.fabrique = fabrique
        self.gestionnaireCommandes = GestionnaireCommandes()
        self.derniereReservation = None

    def reserver(self):
        reservation = self.fabrique.creerReservation()
        commande = CommandeReservation(reservation)
        self.gestionnaireCommandes.executerCommande(commande)
        self.derniereReservation = reservation
        return reservation

    def annuler(self):
        if self.derniereReservation is None:
            print("Aucune réservation à annuler.")
            return

        if not self.derniereReservation.active:
            print("La dernière réservation est déjà annulée.")
            return

        commande = CommandeAnnulation(self.derniereReservation)
        self.gestionnaireCommandes.executerCommande(commande)

    def annulerDerniereAction(self):
        self.gestionnaireCommandes.annuler()

    def retablirDerniereAction(self):
        self.gestionnaireCommandes.retablir()
