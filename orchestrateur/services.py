"""
Interface et Stub du ReservationService et Reservation (Groupe 4).
Conforme au document de référence Python POO de SmartCampus :
- Convention : classes en PascalCase, méthodes/arguments en snake_case.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional


class Reservation(ABC):
    """Interface Reservation du Groupe 4."""

    @abstractmethod
    def reserve(self) -> None:
        """Exécute / active la réservation."""
        pass

    @abstractmethod
    def cancel(self) -> None:
        """Annule la réservation."""
        pass


class ReservationStub(Reservation):
    """Implémentation concrète stub d'une réservation pour tests et démos."""

    def __init__(self, details: str = "Réservation"):
        self.details = details
        self.active = False

    def reserve(self) -> None:
        self.active = True

    def cancel(self) -> None:
        self.active = False

    def __repr__(self) -> str:
        return f"ReservationStub({self.details}, active={self.active})"


class ReservationService(ABC):
    """
    Interface du service de réservation (développé par le Groupe 4).
    Méthodes conformes au référentiel :
    - reserve() -> Reservation
    - cancel() -> None
    - undo_last_action() -> None
    - redo_last_action() -> None
    """

    @abstractmethod
    def reserve(self, *args, **kwargs) -> Reservation:
        pass

    @abstractmethod
    def cancel(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def undo_last_action(self) -> None:
        pass

    @abstractmethod
    def redo_last_action(self) -> None:
        pass


class ReservationServiceStub(ReservationService):
    """Stub simulant le ReservationService du Groupe 4."""

    def __init__(self):
        self.history = []

    def reserve(self, *args, **kwargs) -> Reservation:
        requester_id = kwargs.get("requester_id", args[0] if len(args) > 0 else "inconnu")
        room = kwargs.get("room", args[1] if len(args) > 1 else "salle")
        start_time = kwargs.get("start_time", args[2] if len(args) > 2 else "")
        end_time = kwargs.get("end_time", args[3] if len(args) > 3 else "")

        res = ReservationStub(f"room={room}, requester={requester_id}, from={start_time}, to={end_time}")
        res.reserve()
        self.history.append(res)
        return res

    def cancel(self, *args, **kwargs) -> None:
        if args and isinstance(args[0], Reservation):
            args[0].cancel()
        print(f"[ReservationService (Groupe 4)] Annulation de la réservation effectuée.")

    def undo_last_action(self) -> None:
        print("[ReservationService (Groupe 4)] Annulation de la dernière action (Undo).")

    def redo_last_action(self) -> None:
        print("[ReservationService (Groupe 4)] Rétablissement de la dernière action (Redo).")
