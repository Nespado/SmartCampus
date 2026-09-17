"""
Interface et Stub du ReservationService (Groupe 4).
L'Orchestrateur (Groupe 6) interagit avec le Groupe 4 via la façade SmartCampusFacade.
"""
from abc import ABC, abstractmethod
from typing import Any


class ReservationService(ABC):
    """Interface du service de réservation (développé par le Groupe 4)."""

    @abstractmethod
    def reserve(self, requester_id: str, room: Any, start_time: Any, end_time: Any) -> Any:
        pass

    @abstractmethod
    def cancel(self, reservation: Any) -> None:
        pass


class ReservationServiceStub(ReservationService):
    """Stub simulant le ReservationService du Groupe 4."""

    def reserve(self, requester_id: str, room: Any, start_time: Any, end_time: Any) -> Any:
        return f"Reservation[room={room}, requester={requester_id}, from={start_time}, to={end_time}]"

    def cancel(self, reservation: Any) -> None:
        print(f"[ReservationService (Groupe 4)] Annulation de la réservation : {reservation}")
