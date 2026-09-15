from enum import Enum

from notifications import (
Notification,
SMS,
Email,
Push,
Slack
)
from evenements import Evenement

class TypeNotification(Enum):
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"
    SLACK = "slack"

class NotificationFactory:
    """Fabrique les notifications à partir d'un événement campus."""

    @staticmethod
    def create(event: Evenement | TypeNotification, recipient: str,
               contenu: str | None = None) -> Notification:
        """Crée une notification pour un événement.

        L'ancien appel ``creer(type, destinataire, contenu)`` reste accepté
        afin de ne pas casser les intégrations existantes.
        """
        if isinstance(event, TypeNotification):
            type_notification = event
            contenu = "" if contenu is None else contenu
        else:
            type_notification = TypeNotification.EMAIL
            contenu = event.description if contenu is None else contenu

        if type_notification == TypeNotification.SMS:
            return SMS(recipient, contenu)

        if type_notification == TypeNotification.EMAIL:
            return Email(recipient, contenu)

        if type_notification == TypeNotification.PUSH:
            return Push(recipient, contenu)

        if type_notification == TypeNotification.SLACK:
            return Slack(recipient, contenu)

        raise ValueError(
            f"Type de notification inconnu : {type_notification}"
        )

    @staticmethod
    def creer(type_notification: TypeNotification, destinataire: str,
              contenu: str = "") -> Notification:
        """Alias français de ``create`` pour compatibilité."""
        return NotificationFactory.create(type_notification, destinataire, contenu)
