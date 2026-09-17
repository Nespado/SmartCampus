class GestionnaireCommandes:
    """Conserve l'historique pour annuler ou rétablir les actions."""

    def __init__(self):
        self.historique = []
        self.historiqueRetablissement = []

    def executerCommande(self, commande):
        commande.executer()
        self.historique.append(commande)
        self.historiqueRetablissement.clear()

    def annuler(self):
        if not self.historique:
            print("Aucune action à annuler.")
            return

        commande = self.historique.pop()
        commande.defaire()
        self.historiqueRetablissement.append(commande)

    def retablir(self):
        if not self.historiqueRetablissement:
            print("Aucune action à rétablir.")
            return

        commande = self.historiqueRetablissement.pop()
        commande.executer()
        self.historique.append(commande)
