"""
Tests unitaires pour la façade SmartCampusFacade (Groupe 6).
Valide la délégation et l'interception du contrôle d'accès pour :
- Le Groupe 4 (Réservations)
- Le Groupe 1 (Notifications)
- Le Groupe 5 (Data Management)
- Le Groupe 3 (Contrôle d'accès & Sécurité)
"""
import unittest
from unittest.mock import MagicMock
from orchestrateur import (
    SmartCampusFacade,
    Reservation,
    ReservationService,
    CampusEvent,
    Incendie,
    Notification,
    BaseNotification,
    NotificationService,
    DataManagementService,
    UnifiedData,
    Report,
    AccessControlService,
    AccessRequest,
    AccessDecision,
)


class TestSmartCampusFacade(unittest.TestCase):

    def setUp(self):
        # Mocks des services externes
        self.mock_reservation_service = MagicMock(spec=ReservationService)
        self.mock_notification_service = MagicMock(spec=NotificationService)
        self.mock_data_service = MagicMock(spec=DataManagementService)
        self.mock_access_service = MagicMock(spec=AccessControlService)

        # Par défaut, accès autorisé pour tester les délégations
        self.mock_access_service.check_access.return_value = AccessDecision(allowed=True, reason="Autorisé")

        self.facade = SmartCampusFacade(
            reservation_service=self.mock_reservation_service,
            notification_service=self.mock_notification_service,
            data_service=self.mock_data_service,
            access_service=self.mock_access_service,
        )

    # --------------------------------------------------------------------------
    # TESTS DÉLÉGATION GROUPE 4 — RÉSERVATIONS
    # --------------------------------------------------------------------------

    def test_reserve_room_delegation(self):
        mock_reservation = MagicMock(spec=Reservation)
        self.mock_reservation_service.reserve.return_value = mock_reservation

        result = self.facade.reserve_room("USER_01", "Amphi A", "10:00", "12:00")

        self.assertEqual(result, mock_reservation)
        self.mock_reservation_service.reserve.assert_called_once_with("USER_01", "Amphi A", "10:00", "12:00")

    def test_cancel_reserve_delegation(self):
        mock_reservation = MagicMock(spec=Reservation)

        self.facade.cancel_reserve("USER_01", mock_reservation)

        self.mock_reservation_service.cancel.assert_called_once_with(mock_reservation)

    def test_undo_last_action_delegation(self):
        self.facade.undo_last_action("USER_01")
        self.mock_reservation_service.undo_last_action.assert_called_once()

    def test_redo_last_action_delegation(self):
        self.facade.redo_last_action("USER_01")
        self.mock_reservation_service.redo_last_action.assert_called_once()

    # --------------------------------------------------------------------------
    # TESTS DÉLÉGATION GROUPE 1 — NOTIFICATIONS
    # --------------------------------------------------------------------------

    def test_update_notification_delegation(self):
        event = Incendie(localisation="Bâtiment C", description="Départ de flammes")

        self.facade.update_notification("USER_01", event)

        self.mock_notification_service.update.assert_called_once_with(event)

    def test_handle_event_notification_delegation(self):
        event = Incendie(localisation="Bâtiment A", description="Fumée suspecte")

        self.facade.handle_event_notification("USER_01", event)

        self.mock_notification_service.handle_event.assert_called_once_with(event)

    def test_send_notification_delegation(self):
        notification = BaseNotification(recipient="admin@campus.fr", content="Message urgent")

        self.facade.send_notification("USER_01", notification)

        self.mock_notification_service.send.assert_called_once_with(notification)

    # --------------------------------------------------------------------------
    # TESTS DÉLÉGATION GROUPE 5 — DATA MANAGEMENT
    # --------------------------------------------------------------------------

    def test_import_data_delegation(self):
        mock_unified = MagicMock(spec=UnifiedData)
        self.mock_data_service.import_data.return_value = mock_unified

        result = self.facade.import_data("USER_01")

        self.assertEqual(result, mock_unified)
        self.mock_data_service.import_data.assert_called_once()

    def test_retrieve_data_delegation(self):
        mock_unified = MagicMock(spec=UnifiedData)
        self.mock_data_service.retrieve_data.return_value = mock_unified

        result = self.facade.retrieve_data("USER_01")

        self.assertEqual(result, mock_unified)
        self.mock_data_service.retrieve_data.assert_called_once()

    def test_generate_report_delegation(self):
        mock_report = MagicMock(spec=Report)
        self.mock_data_service.generate_report.return_value = mock_report

        result = self.facade.generate_report("USER_01")

        self.assertEqual(result, mock_report)
        self.mock_data_service.generate_report.assert_called_once()

    # --------------------------------------------------------------------------
    # TESTS DÉLÉGATION GROUPE 3 — CONTRÔLE D'ACCÈS
    # --------------------------------------------------------------------------

    def test_check_access_delegation(self):
        mock_request = MagicMock(spec=AccessRequest)
        mock_decision = MagicMock(spec=AccessDecision)
        self.mock_access_service.check_access.return_value = mock_decision

        result = self.facade.check_access(mock_request)

        self.assertEqual(result, mock_decision)
        self.mock_access_service.check_access.assert_called_once_with(mock_request)

    # --------------------------------------------------------------------------
    # TESTS INTERCEPTION ET GESTION DES REFUS D'ACCÈS (_check_access)
    # --------------------------------------------------------------------------

    def test_reserve_room_permission_denied_raises_error(self):
        self.mock_access_service.check_access.return_value = AccessDecision(allowed=False, reason="Droits insuffisants")

        with self.assertRaises(PermissionError) as ctx:
            self.facade.reserve_room("STUDENT_99", "Amphi A", "10:00", "12:00")

        self.assertIn("Accès refusé pour STUDENT_99", str(ctx.exception))
        # Le service de réservation ne doit pas avoir été appelé
        self.mock_reservation_service.reserve.assert_not_called()

    def test_cancel_reserve_permission_denied_raises_error(self):
        self.mock_access_service.check_access.return_value = AccessDecision(allowed=False, reason="Refusé")

        with self.assertRaises(PermissionError):
            self.facade.cancel_reserve("STUDENT_99", MagicMock())

        self.mock_reservation_service.cancel.assert_not_called()

    def test_import_data_permission_denied_raises_error(self):
        self.mock_access_service.check_access.return_value = AccessDecision(allowed=False, reason="Interdit")

        with self.assertRaises(PermissionError):
            self.facade.import_data("GUEST")

        self.mock_data_service.import_data.assert_not_called()


if __name__ == "__main__":
    unittest.main()
