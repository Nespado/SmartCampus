"""
Tests unitaires pour la façade SmartCampusFacade (Groupe 6 -> Groupe 4).
"""
import unittest
from unittest.mock import MagicMock
from orchestrateur import SmartCampusFacade
from orchestrateur.services import ReservationService


class TestSmartCampusFacade(unittest.TestCase):

    def setUp(self):
        # Mock du service de réservation du Groupe 4
        self.mock_reservation_service = MagicMock(spec=ReservationService)

        # Injection du mock dans la façade
        self.facade = SmartCampusFacade(
            reservation_service=self.mock_reservation_service,
        )

    def test_reserve_room_delegation(self):
        self.mock_reservation_service.reserve.return_value = "ReservationObject"

        result = self.facade.reserve_room("USER_01", "Amphi A", "10:00", "12:00")

        self.assertEqual(result, "ReservationObject")
        self.mock_reservation_service.reserve.assert_called_once_with("USER_01", "Amphi A", "10:00", "12:00")

    def test_cancel_reserve_delegation(self):
        reservation = "ReservationObject"

        self.facade.cancel_reserve(reservation)

        self.mock_reservation_service.cancel.assert_called_once_with(reservation)


if __name__ == "__main__":
    unittest.main()
