"""
Tests unitaires pour la façade SmartCampusFacade (Groupe 6 -> Groupe 4).
Conforme aux conventions de nommage et aux signatures du référentiel.
"""
import unittest
from unittest.mock import MagicMock
from orchestrateur import SmartCampusFacade
from orchestrateur.services import Reservation, ReservationService


class TestSmartCampusFacade(unittest.TestCase):

    def setUp(self):
        self.mock_reservation_service = MagicMock(spec=ReservationService)
        self.facade = SmartCampusFacade(
            reservation_service=self.mock_reservation_service,
        )

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


if __name__ == "__main__":
    unittest.main()
