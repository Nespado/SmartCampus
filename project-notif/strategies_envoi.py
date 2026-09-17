from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notifications import Notification


class DeliveryStrategy(ABC):
    """Interface de stratégie d'envoi (Groupe 1)."""

    @abstractmethod
    def send(self, notification: 'Notification') -> None:
        pass

    def envoyer(self, notification: 'Notification') -> None:
        """Alias français pour compatibilité."""
        self.send(notification)


# Alias français pour compatibilité
StrategieEnvoi = DeliveryStrategy


class SmsDeliveryStrategy(DeliveryStrategy):

    def send(self, notification: 'Notification') -> None:
        print(f"[STRATÉGIE SMS] Envoi en cours à {notification.destinataire}...")


class EmailDeliveryStrategy(DeliveryStrategy):

    def send(self, notification: 'Notification') -> None:
        print(f"[STRATÉGIE EMAIL] Envoi en cours à {notification.destinataire}...")


class PushDeliveryStrategy(DeliveryStrategy):

    def send(self, notification: 'Notification') -> None:
        print(f"[STRATÉGIE PUSH] Envoi en cours à {notification.destinataire}...")


class SlackDeliveryStrategy(DeliveryStrategy):

    def send(self, notification: 'Notification') -> None:
        print(f"[STRATÉGIE SLACK] Envoi en cours à {notification.destinataire}...")


# Alias français conservés
EnvoiSMS = SmsDeliveryStrategy
EnvoiEmail = EmailDeliveryStrategy
EnvoiPush = PushDeliveryStrategy
EnvoiSlack = SlackDeliveryStrategy

__all__ = [
    "DeliveryStrategy",
    "StrategieEnvoi",
    "SmsDeliveryStrategy",
    "EmailDeliveryStrategy",
    "PushDeliveryStrategy",
    "SlackDeliveryStrategy",
    "EnvoiSMS",
    "EnvoiEmail",
    "EnvoiPush",
    "EnvoiSlack",
]