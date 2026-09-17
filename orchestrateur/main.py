"""
Client (GROUPE 6 — ORCHESTRATEUR)
Point d'entrée unique représentant le Client (Admin / Étudiant) interagissant avec la Façade SmartCampusFacade.
Démontre l'utilisation des services de Réservation (Groupe 4), de Notification (Groupe 1) et de Gestion des données (Groupe 5).
"""
from datetime import datetime, timedelta
from orchestrateur import (
    SmartCampusFacade,
    Incendie,
    CoursAnnule,
    BaseNotification,
)


class Client:
    """Représente le Client interagissant uniquement avec SmartCampusFacade."""

    def __init__(self, facade: SmartCampusFacade):
        self.facade = facade

    def run_demo(self):
        print("=" * 70)
        print("  SMARTCAMPUS — CLIENT & FAÇADE (GROUPES 4 RÉSERVATION, 1 NOTIF & 5 DATA)")
        print("=" * 70)

        # ----------------------------------------------------------------------
        # PARTIE 1 : RÉSERVATIONS (GROUPE 4)
        # ----------------------------------------------------------------------
        print("\n--- [PARTIE 1 : RÉSERVATIONS (Groupe 4)] ---")

        # 1. Demande de réservation
        print("\n[1.1] Demande de réservation d'une salle via la Façade...")
        now = datetime.now()
        start = (now + timedelta(hours=1)).strftime("%H:%M")
        end = (now + timedelta(hours=3)).strftime("%H:%M")

        reservation = self.facade.reserve_room(
            requester_id="STUDENT_42",
            room="Amphi Turing",
            start_time=start,
            end_time=end,
        )
        print(f"      Résultat retourné : {reservation}")

        # 2. Undo / Redo
        print("\n[1.2] Test Undo / Redo via la Façade...")
        self.facade.undo_last_action()
        self.facade.redo_last_action()

        # 3. Annulation
        print("\n[1.3] Annulation de la réservation via la Façade...")
        self.facade.cancel_reserve(reservation)

        # ----------------------------------------------------------------------
        # PARTIE 2 : NOTIFICATIONS (GROUPE 1)
        # ----------------------------------------------------------------------
        print("\n--- [PARTIE 2 : NOTIFICATIONS (Groupe 1)] ---")

        # 1. Notification suite à un événement (Pattern Observer via Façade)
        print("\n[2.1] Signalement d'un événement campus (update_notification)...")
        event_incendie = Incendie(localisation="Bâtiment B - Étage 2", description="Départ de feu détecté")
        self.facade.update_notification(event_incendie)

        # 2. Traitement d'un événement direct (handle_event_notification)
        print("\n[2.2] Traitement direct d'un événement (handle_event_notification)...")
        event_cours = CoursAnnule(nom_cours="Architecture Logicielle", raison="Absence de l'enseignant")
        self.facade.handle_event_notification(event_cours)

        # 3. Envoi direct d'une notification (send_notification)
        print("\n[2.3] Envoi direct d'une notification (send_notification)...")
        notification = BaseNotification(
            recipient="etudiants@campus.fr",
            content="Rappel : fermeture exceptionnelle de la bibliothèque universitaire à 18h."
        )
        self.facade.send_notification(notification)

        # ----------------------------------------------------------------------
        # PARTIE 3 : GESTION DES DONNÉES (GROUPE 5)
        # ----------------------------------------------------------------------
        print("\n--- [PARTIE 3 : GESTION DES DONNÉES (Groupe 5)] ---")

        # 1. Importation des données via la Façade
        print("\n[3.1] Importation des données via SmartCampusFacade...")
        unified_data = self.facade.import_data()
        print(f"      Données retournées : {unified_data}")

        # 2. Récupération des données via la Façade
        print("\n[3.2] Récupération des données via SmartCampusFacade...")
        data = self.facade.retrieve_data()
        print(f"      Données récupérées : {data}")

        # 3. Génération d'un rapport via la Façade
        print("\n[3.3] Génération d'un rapport via SmartCampusFacade...")
        report = self.facade.generate_report()
        print(f"      Rapport généré : {report}")

        print("\n" + "=" * 70)
        print("  DÉMONSTRATION DU CLIENT ET DE LA FAÇADE RÉUSSIE")
        print("=" * 70)


def main():
    facade = SmartCampusFacade()
    client = Client(facade)
    client.run_demo()


if __name__ == "__main__":
    main()