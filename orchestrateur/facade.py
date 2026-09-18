"""
SmartCampusFacade (GROUPE 6 — ORCHESTRATEUR)
Façade orchestrateur unifiée intégrant :
- Le Groupe 4 : Réservation (ReservationService)
- Le Groupe 1 : Notifications (NotificationService)
- Le Groupe 5 : Gestion des données (DataManagementService)

Conforme aux conventions de nommage :
- Classes en PascalCase
- Méthodes et arguments en snake_case
"""
from typing import Any, Optional
from orchestrateur.services import (
    Reservation,
    ReservationService,
    ReservationServiceStub,

    CampusEvent,
    Notification,
    NotificationService,
    NotificationServiceStub,

    DataManagementService,
    DataManagementServiceStub,
    UnifiedData,
    Report,

    AccessControlService,
    AccessControlServiceStub,
    AccessRequest,
    AccessDecision,
)


class SmartCampusFacade:
    """
    Façade unique du système SmartCampus (Groupe 6).
    Point d'entrée orchestrant les requêtes vers les microservices :
    - Groupe 4 (Réservations)
    - Groupe 1 (Notifications)
    - Groupe 5 (Gestion des données)
    """

    def __init__(
        self,
        reservation_service: Optional[ReservationService] = None,
        notification_service: Optional[NotificationService] = None,
        data_service: Optional[DataManagementService] = None,
        access_service : Optional[AccessControlService] = None
    ):
        self.reservation_service = reservation_service or ReservationServiceStub()
        self.notification_service = notification_service or NotificationServiceStub()
        self.data_service = data_service or DataManagementServiceStub()
        self.access_service = access_service or AccessControlServiceStub()

    # ==========================================================================
    # MÉTHODES GROUPE 4 — RESERVATION
    # ==========================================================================

    def reserve_room(
            self,
            requester_id: str,
            room: Any,
            start_time: Any,
            end_time: Any
    ) -> Reservation:
        """Vérifie l'accès puis délègue la réservation au ReservationService."""

        self._check_access(
            user_id=requester_id,
            resource=room,
            action="reserve"
        )

        return self.reservation_service.reserve(
            requester_id,
            room,
            start_time,
            end_time
        )

    def cancel_reserve(
            self,
            requester_id: str,
            reservation: Any = None
    ) -> None:
        """Vérifie l'accès puis délègue l'annulation."""

        self._check_access(
            user_id=requester_id,
            resource="reservation",
            action="cancel"
        )

        self.reservation_service.cancel(reservation)

    def undo_last_action(self, user_id: str) -> None:
        """Vérifie l'accès puis délègue l'action Undo."""

        self._check_access(
            user_id=user_id,
            resource="reservation",
            action="undo"
        )

        self.reservation_service.undo_last_action()

    def redo_last_action(self, user_id: str) -> None:
        """Vérifie l'accès puis délègue l'action Redo."""

        self._check_access(
            user_id=user_id,
            resource="reservation",
            action="redo"
        )

        self.reservation_service.redo_last_action()

    # ==========================================================================
    # MÉTHODES GROUPE 1 — NOTIFICATIONS
    # ==========================================================================

    def update_notification(
            self,
            user_id: str,
            event: CampusEvent
    ) -> None:
        """Vérifie l'accès puis met à jour les notifications."""

        self._check_access(
            user_id=user_id,
            resource="notification",
            action="update"
        )

        self.notification_service.update(event)

    def handle_event_notification(
            self,
            user_id: str,
            event: CampusEvent
    ) -> None:
        """Vérifie l'accès puis traite l'événement."""

        self._check_access(
            user_id=user_id,
            resource="notification",
            action="handle"
        )

        self.notification_service.handle_event(event)

    def send_notification(
            self,
            user_id: str,
            notification: Notification
    ) -> None:
        """Vérifie l'accès puis envoie la notification."""

        self._check_access(
            user_id=user_id,
            resource="notification",
            action="send"
        )

        self.notification_service.send(notification)

    # ==========================================================================
    # MÉTHODES GROUPE 5 — DATA MANAGEMENT
    # ==========================================================================

    def import_data(self, user_id: str) -> UnifiedData:
        """Vérifie l'accès puis délègue l'importation des données."""

        self._check_access(
            user_id=user_id,
            resource="data",
            action="import"
        )

        return self.data_service.import_data()

    def retrieve_data(self, user_id: str) -> UnifiedData:
        """Vérifie l'accès puis délègue la récupération des données."""

        self._check_access(
            user_id=user_id,
            resource="data",
            action="retrieve"
        )

        return self.data_service.retrieve_data()

    def generate_report(self, user_id: str) -> Report:
        """Vérifie l'accès puis délègue la génération du rapport."""

        self._check_access(
            user_id=user_id,
            resource="data",
            action="generate_report"
        )

        return self.data_service.generate_report()

    # ==========================================================================
    # MÉTHODES GROUPE 3 — CONTRÔLE D'ACCÈS
    # ==========================================================================

    def check_access(self, request: AccessRequest) -> AccessDecision:
        """Délègue la vérification des droits d'accès à l'AccessControlService."""
        return self.access_service.check_access(request)

    def _check_access(
            self,
            user_id: str,
            resource: str,
            action: str
    ) -> None:
        """Vérifie que l'utilisateur est autorisé à effectuer l'action."""

        request = AccessRequest(
            user_id=user_id,
            resource=resource,
            action=action
        )

        decision = self.access_service.check_access(request)

        if not decision.allowed:
            raise PermissionError(
                f"Accès refusé pour {user_id} : {decision.reason}"
            )

