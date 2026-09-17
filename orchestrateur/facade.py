"""
SmartCampusFacade (GROUPE 6 — ORCHESTRATEUR)
Façade orchestrateur focalisée sur l'intégration du service de réservation (Groupe 4).
"""
from typing import Any, Optional
from orchestrateur.services import ReservationService, ReservationServiceStub


class SmartCampusFacade:
    """
    Façade unique du système SmartCampus (Groupe 6).
    Point d'entrée orchestrant les requêtes de réservation vers le Groupe 4 (ReservationService).
    """

    def __init__(
        self,
        reservation_service: Optional[ReservationService] = None,
    ):
        self.reservation_service = reservation_service or ReservationServiceStub()

    # --- GROUPE 4 : RESERVATION ---
    def reserve_room(self, requester_id: str, room: Any, start_time: Any, end_time: Any) -> Any:
        """Réserve une salle en déléguant au ReservationService du Groupe 4."""
        return self.reservation_service.reserve(requester_id, room, start_time, end_time)

    def cancel_reserve(self, reservation: Any) -> None:
        """Annule une réservation en déléguant au ReservationService du Groupe 4."""
        self.reservation_service.cancel(reservation)
