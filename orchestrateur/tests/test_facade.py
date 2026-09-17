"""
Tests unitaires pour la façade SmartCampusFacade (Groupe 6).
Valide la délégation vers le Groupe 4 (Réservations), le Groupe 1 (Notifications) et le Groupe 5 (Data Management).
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
)


class TestSmartCampusFacade(unittest.TestCase):

    def setUp(self):
        # Mocks des services externes
        self.mock_reservation_service = MagicMock(spec=ReservationService)
        self.mock_notification_service = MagicMock(spec=NotificationService)
        self.mock_data_service = MagicMock(spec=DataManagementService)

        self.facade = SmartCampusFacade(
            reservation_service=self.mock_reservation_service,
            notification_service=self.mock_notification_service,
            data_service=self.mock_data_service,
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

        self.facade.cancel_reserve(mock_reservation)

        self.mock_reservation_service.cancel.assert_called_once_with(mock_reservation)

    def test_undo_last_action_delegation(self):
        self.facade.undo_last_action()
        self.mock_reservation_service.undo_last_action.assert_called_once()

    def test_redo_last_action_delegation(self):
        self.facade.redo_last_action()
        self.mock_reservation_service.redo_last_action.assert_called_once()

    # --------------------------------------------------------------------------
    # TESTS DÉLÉGATION GROUPE 1 — NOTIFICATIONS
    # --------------------------------------------------------------------------

    def test_update_notification_delegation(self):
        event = Incendie(localisation="Bâtiment C", description="Départ de flammes")

        self.facade.update_notification(event)

        self.mock_notification_service.update.assert_called_once_with(event)

    def test_handle_event_notification_delegation(self):
        event = Incendie(localisation="Bâtiment A", description="Fumée suspecte")

        self.facade.handle_event_notification(event)

        self.mock_notification_service.handle_event.assert_called_once_with(event)

    def test_send_notification_delegation(self):
        notification = BaseNotification(recipient="admin@campus.fr", content="Message urgent")

        self.facade.send_notification(notification)

        self.mock_notification_service.send.assert_called_once_with(notification)

    # --------------------------------------------------------------------------
    # TESTS DÉLÉGATION GROUPE 5 — DATA MANAGEMENT
    # --------------------------------------------------------------------------

    def test_import_data_delegation(self):
        mock_unified = MagicMock(spec=UnifiedData)
        self.mock_data_service.import_data.return_value = mock_unified

        result = self.facade.import_data()

        self.assertEqual(result, mock_unified)
        self.mock_data_service.import_data.assert_called_once()

    def test_retrieve_data_delegation(self):
        mock_unified = MagicMock(spec=UnifiedData)
        self.mock_data_service.retrieve_data.return_value = mock_unified

        result = self.facade.retrieve_data()

        self.assertEqual(result, mock_unified)
        self.mock_data_service.retrieve_data.assert_called_once()

    def test_generate_report_delegation(self):
        mock_report = MagicMock(spec=Report)
        self.mock_data_service.generate_report.return_value = mock_report

        result = self.facade.generate_report()

        self.assertEqual(result, mock_report)
        self.mock_data_service.generate_report.assert_called_once()


if __name__ == "__main__":
    unittest.main()
