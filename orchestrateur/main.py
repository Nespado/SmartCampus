"""
Client (GROUPE 6 — ORCHESTRATEUR)
Point d'entrée unique représentant le Client (Admin / Étudiant) effectuant des réservations via SmartCampusFacade.
"""
from datetime import datetime, timedelta
from orchestrateur import SmartCampusFacade


class Client:
    """Représente le Client (Interface Admin ou Étudiant) interagissant avec la Façade."""

    def __init__(self, facade: SmartCampusFacade):
        self.facade = facade

    def run_demo(self):
        print("=" * 60)
        print("   SMARTCAMPUS — CLIENT & FACADE (INTEGRATION GROUPE 4 - RESERVATION)")
        print("=" * 60)

        # 1. Réservation d'une salle via la Façade
        print("\n[1] Demande de réservation d'une salle via SmartCampusFacade...")
        now = datetime.now()
        start = (now + timedelta(hours=1)).strftime("%H:%M")
        end = (now + timedelta(hours=3)).strftime("%H:%M")

        reservation = self.facade.reserve_room(
            requester_id="STUDENT_42",
            room="Amphi Turing",
            start_time=start,
            end_time=end,
        )
        print(f"    Résultat retourné par la Façade : {reservation}")

        # 2. Undo / Redo via la Façade
        print("\n[2] Test Undo / Redo via SmartCampusFacade...")
        self.facade.undo_last_action()
        self.facade.redo_last_action()

        # 3. Annulation de la réservation via la Façade
        print("\n[3] Demande d'annulation de la réservation via SmartCampusFacade...")
        self.facade.cancel_reserve(reservation)

        print("\n" + "=" * 60)
        print("   DEMONSTRATION FACADE / GROUPE 4 COMPLÉTÉE")
        print("=" * 60)

        # 4. Importation des données via la Façade
        print("\n[4] Importation des données via SmartCampusFacade...")

        unified_data = self.facade.import_data()

        print(f"    Données retournées : {unified_data}")

        # 5. Récupération des données via la Façade
        print("\n[5] Récupération des données via SmartCampusFacade...")

        data = self.facade.retrieve_data()

        print(f"    Données récupérées : {data}")

        # 6. Génération d'un rapport via la Façade
        print("\n[6] Génération d'un rapport via SmartCampusFacade...")

        report = self.facade.generate_report()

        print(f"    Rapport généré : {report}")


def main():
    facade = SmartCampusFacade()
    client = Client(facade)
    client.run_demo()


if __name__ == "__main__":
    main()