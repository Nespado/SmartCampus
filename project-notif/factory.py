from enum import Enum

from notifications import (
    Notification,
    SMS,
    Email,
    Push,
    Slack,
    BaseNotification,
)
from evenements import CampusEvent, Evenement


class TypeNotification(Enum):
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"
    SLACK = "slack"


class NotificationFactory:
    """Fabrique les notifications à partir d'un événement campus (Groupe 1)."""

    @staticmethod
    def create(
        event: CampusEvent | TypeNotification,
        recipient: str,
        contenu: str | None = None,
    ) -> Notification:
        """Crée une notification pour un événement ou selon un type.

        Conforme au contrat Groupe 1 :
            create(event: CampusEvent, recipient: str) -> Notification
        """
        if isinstance(event, TypeNotification):
            type_notification = event
            body = "" if contenu is None else contenu
        else:
            type_notification = TypeNotification.EMAIL
            if contenu is not None:
                body = contenu
            elif hasattr(event, "description"):
                body = event.description
            else:
                body = str(event)

        if type_notification == TypeNotification.SMS:
            return SMS(destinataire=recipient, contenu=body)

        if type_notification == TypeNotification.EMAIL:
            return Email(destinataire=recipient, contenu=body)

        if type_notification == TypeNotification.PUSH:
            return Push(destinataire=recipient, contenu=body)

        if type_notification == TypeNotification.SLACK:
            return Slack(destinataire=recipient, contenu=body)

        raise ValueError(
            f"Type de notification inconnu : {type_notification}"
        )

    @staticmethod
    def creer(
        type_notification: TypeNotification,
        destinataire: str,
        contenu: str = "",
    ) -> Notification:
        """Alias français de ``create`` pour compatibilité."""
        return NotificationFactory.create(type_notification, destinataire, contenu)


__all__ = [
    "NotificationFactory",
    "TypeNotification",
]
