"""
SmartCampusFacade (GROUPE 6 — ORCHESTRATEUR)
Façade orchestrateur conforme aux conventions de nommage :
- Classes en PascalCase
- Méthodes et arguments en snake_case
"""
from typing import Any, Optional

from orchestrateur.services import (
    Reservation,
    ReservationService,
    ReservationServiceStub,
    DataManagementService,
    DataManagementServiceStub,
    UnifiedData,
    Report,
)


class SmartCampusFacade:
    """
    Façade unique du système SmartCampus (Groupe 6).
    Point d'entrée orchestrant les requêtes de réservation vers le Groupe 4 (ReservationService).
    """

    def __init__(
        self,
        reservation_service: Optional[ReservationService] = None,
        data_service: Optional[DataManagementService] = None,
    ):
        self.reservation_service = reservation_service or ReservationServiceStub()
        self.data_service = (
                data_service or DataManagementServiceStub()
        )

    # --- GROUPE 4 : RESERVATION ---
    def reserve_room(self, requester_id: str, room: Any, start_time: Any, end_time: Any) -> Reservation:
        """Réserve une salle en déléguant au ReservationService du Groupe 4."""
        return self.reservation_service.reserve(requester_id, room, start_time, end_time)

    def cancel_reserve(self, reservation: Any = None) -> None:
        """Annule une réservation en déléguant au ReservationService du Groupe 4."""
        self.reservation_service.cancel(reservation)

    def undo_last_action(self) -> None:
        """Délègue l'annulation de la dernière action (Undo) au ReservationService du Groupe 4."""
        self.reservation_service.undo_last_action()

    def redo_last_action(self) -> None:
        """Délègue le rétablissement de la dernière action (Redo) au ReservationService du Groupe 4."""
        self.reservation_service.redo_last_action()

    # --- DATA MANAGEMENT ---
    def import_data(self) -> UnifiedData:
        """Délègue l'importation des données au DataManagementService."""
        return self.data_service.import_data()

    def retrieve_data(self) -> UnifiedData:
        """Délègue la récupération des données au DataManagementService."""
        return self.data_service.retrieve_data()

    def generate_report(self) -> Report:
        """Délègue la génération du rapport au DataManagementService."""
        return self.data_service.generate_report()