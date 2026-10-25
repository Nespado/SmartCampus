"""
Tests d'intégration validant la connexion de la Façade SmartCampus
avec les services réels des différents groupes :
- Groupe 1 : Notifications
- Groupe 2 : Bâtiment intelligent / Régulation
- Groupe 3 : Contrôle d'accès
- Groupe 4 : Réservations
- Groupe 5 : Gestion des données
"""
import unittest
from datetime import datetime, timedelta, date

from orchestrateur.facade import SmartCampusFacade
from orchestrateur.services import Incendie, CoursAnnule, BaseNotification


class IntegrationConnectedServicesTestCase(unittest.TestCase):
    """Vérifie l'interaction de bout en bout de la Façade avec les vrais services."""

    def setUp(self):
        self.facade = SmartCampusFacade.create_with_real_services()
        self.student_id = "STUDENT_42"
        self.admin_id = "ADMIN_01"

    def test_reservation_service_integration(self):
        """Vérifie la réservation réelle via la Façade."""
        start = datetime.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)

        reservation = self.facade.reserve_room(
            requester_id=self.student_id,
            room="Salle B204",
            start_time=start,
            end_time=end,
        )
        self.assertIsNotNone(reservation)

        # Annulation et undo/redo
        self.facade.undo_last_action(self.student_id)
        self.facade.redo_last_action(self.student_id)
        self.facade.cancel_reserve(self.student_id, reservation)

    def test_notification_service_integration(self):
        """Vérifie les événements et notifications via le vrai service project-notif."""
        # Update event
        event = Incendie(localisation="Bâtiment C", description="Détection fumée")
        self.facade.update_notification(self.student_id, event)

        # Handle direct event
        course_event = CoursAnnule(nom_cours="Maths", raison="Professeur absent")
        self.facade.handle_event_notification(self.student_id, course_event)

        # Direct send
        notif = BaseNotification(recipient="info@campus.fr", content="Message test")
        self.facade.send_notification(self.student_id, notif)

    def test_data_management_service_integration(self):
        """Vérifie l'import et le rapport via le vrai service data_management."""
        # Seul admin est autorisé
        with self.assertRaises(PermissionError):
            self.facade.import_data(self.student_id)

        data = self.facade.import_data(self.admin_id)
        self.assertIsNotNone(data)

        retrieved = self.facade.retrieve_data(self.admin_id)
        self.assertIsNotNone(retrieved)

        report = self.facade.generate_report(self.admin_id)
        self.assertIsNotNone(report)

    def test_building_regulation_integration(self):
        """Vérifie la création et régulation d'une salle avec project_building."""
        building_svc = self.facade.building_service
        self.assertIsNotNone(building_svc)

        room = building_svc.create_room("Lab Info", "laboratory", target_temp=22.0, current_temp=19.0)
        building_svc.regulate(room)
        self.assertGreaterEqual(room.heating_level, 0.0)
        self.assertEqual(room.lighting_level, 1.0)


if __name__ == "__main__":
    unittest.main()
