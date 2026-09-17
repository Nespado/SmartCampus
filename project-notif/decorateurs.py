from abc import ABC, abstractmethod

from notifications import Notification, BaseNotification


class NotificationDecorator(Notification, ABC):
    """Décorateur abstrait qui enveloppe une notification (Groupe 1)."""

    def __init__(self, notification: Notification):
        super().__init__(
            destinataire=notification.destinataire,
            contenu=notification.contenu,
        )
        self.notification = notification

    @abstractmethod
    def generate_content(self) -> str:
        pass


class WithSignature(NotificationDecorator):
    """Ajoute une signature à la notification."""

    def __init__(self, notification: Notification, signature: str):
        super().__init__(notification)
        self.signature = signature

    def generate_content(self) -> str:
        return (
            f"{self.notification.generate_content()}\n"
            f"Signature : {self.signature}"
        )


class WithUrgentHeader(NotificationDecorator):
    """Ajoute un en-tête URGENT à la notification."""

    def generate_content(self) -> str:
        return (
            f"URGENT\n"
            f"{self.notification.generate_content()}"
        )


class EncryptedNotification(NotificationDecorator):
    """Chiffre le contenu de la notification (Groupe 1)."""

    def encrypt(self, contenu: str | None = None) -> str:
        """Chiffre le contenu.
        
        Conforme au contrat Groupe 1 : peut être appelé sans argument
        pour chiffrer le contenu de la notification enveloppée.
        Accepte aussi un argument optionnel pour compatibilité.
        """
        if contenu is None:
            contenu = self.notification.generate_content()
        return f"[CHIFFRÉ] {contenu}"

    def generate_content(self) -> str:
        return self.encrypt()

    def chiffrer(self, contenu: str | None = None) -> str:
        """Alias français pour compatibilité."""
        return self.encrypt(contenu)


__all__ = [
    "NotificationDecorator",
    "BaseNotification",
    "WithSignature",
    "WithUrgentHeader",
    "EncryptedNotification",
]
