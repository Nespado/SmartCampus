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
    # MÉTHODES GROUPE 4 — RÉSERVATIONS
    # ==========================================================================

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

    # ==========================================================================
    # MÉTHODES GROUPE 1 — NOTIFICATIONS
    # ==========================================================================

    def update_notification(self, event: CampusEvent) -> None:
        """Met à jour les notifications lors d'un événement campus (Observer update)."""
        self.notification_service.update(event)

    def handle_event_notification(self, event: CampusEvent) -> None:
        """Déclenche le traitement direct d'un événement par le NotificationService."""
        self.notification_service.handle_event(event)

    def send_notification(self, notification: Notification) -> None:
        """Envoie directement une notification via les canaux configurés."""
        self.notification_service.send(notification)

    # ==========================================================================
    # MÉTHODES GROUPE 5 — DATA MANAGEMENT
    # ==========================================================================

    def import_data(self) -> UnifiedData:
        """Délègue l'importation des données au DataManagementService."""
        return self.data_service.import_data()

    def retrieve_data(self) -> UnifiedData:
        """Délègue la récupération des données au DataManagementService."""
        return self.data_service.retrieve_data()

    def generate_report(self) -> Report:
        """Délègue la génération du rapport au DataManagementService."""
        return self.data_service.generate_report()

    # ==========================================================================
    # MÉTHODES GROUPE 3 — CONTRÔLE D'ACCÈS
    # ==========================================================================

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

        decision = self.check_access(request)

        if not decision.allowed:
            raise PermissionError(
                f"Accès refusé pour {user_id} : {decision.reason}"
            )

