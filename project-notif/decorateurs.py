from abc import ABC, abstractmethod

from notifications import Notification

class NotificationDecorator(Notification, ABC):
    """Décorateur abstrait qui enveloppe une notification."""
    def __init__(self, notification: Notification):
        super().__init__(
            notification.destinataire,
            notification.contenu
        )
        self.notification = notification

    @abstractmethod
    def generate_content(self) -> str:
        pass


class BaseNotification(Notification):
    def generate_content(self) -> str:
        return self.contenu


class WithSignature(NotificationDecorator):
    def __init__(
        self,
        notification: Notification,
        signature: str
    ):
        super().__init__(notification)
        self.signature = signature

    def generate_content(self) -> str:
        return (
            f"{self.notification.generate_content()}\n"
            f"Signature : {self.signature}"
        )


class WithUrgentHeader(NotificationDecorator):
    def generate_content(self) -> str:
        return (
            f"URGENT\n"
            f"{self.notification.generate_content()}"
        )


class EncryptedNotification(NotificationDecorator):
    def generate_content(self) -> str:
        return self.encrypt(self.notification.generate_content())

    def encrypt(self, contenu: str) -> str:
        return f"[CHIFFRÉ] {contenu}"

    def chiffrer(self, contenu: str) -> str:
        """Alias français conservé pour l'ancien contrat."""
        return self.encrypt(contenu)

