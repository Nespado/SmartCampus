from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notifications import Notification


class StrategieEnvoi(ABC):
    """Interface de stratégie d'envoi"""
    @abstractmethod
    def send(self, notification: 'Notification'):
        pass

    def envoyer(self, notification: 'Notification'):
        self.send(notification)


class EnvoiSMS(StrategieEnvoi):
    def send(self, notification: 'Notification'):
        print(f"[STRATÉGIE SMS] Envoi en cours à {notification.destinataire}...")


class EnvoiEmail(StrategieEnvoi):
    def send(self, notification: 'Notification'):
        print(f"[STRATÉGIE EMAIL] Envoi en cours à {notification.destinataire}...")


class EnvoiPush(StrategieEnvoi):
    def send(self, notification: 'Notification'):
        print(f"[STRATÉGIE PUSH] Envoi en cours à {notification.destinataire}...")


class EnvoiSlack(StrategieEnvoi):
    def send(self, notification: 'Notification'):
        print(f"[STRATÉGIE SLACK] Envoi en cours à {notification.destinataire}...")


# Noms anglais du contrat Groupe 1.
DeliveryStrategy = StrategieEnvoi
SmsDeliveryStrategy = EnvoiSMS
EmailDeliveryStrategy = EnvoiEmail
PushDeliveryStrategy = EnvoiPush
SlackDeliveryStrategy = EnvoiSlack