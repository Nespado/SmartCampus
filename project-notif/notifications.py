from abc import ABC, abstractmethod


class Notification(ABC):
    """Classe abstraite représentant une notification (Groupe 1)."""

    def __init__(
        self,
        destinataire: str = "",
        contenu: str = "",
        recipient: str | None = None,
        content: str | None = None,
    ):
        target = recipient if recipient is not None else destinataire
        text = content if content is not None else contenu
        self.destinataire = target
        self.recipient = target
        self.contenu = text
        self.content = text

    @abstractmethod
    def generate_content(self) -> str:
        """Génère le contenu textuel de la notification."""
        pass

    def generer_contenu(self) -> str:
        """Alias français pour compatibilité."""
        return self.generate_content()


class BaseNotification(Notification):
    """Notification concrète de base sans décoration (Groupe 1)."""

    def generate_content(self) -> str:
        return self.contenu


class SMS(Notification):

    def generate_content(self) -> str:
        return f"SMS: {self.contenu}"


class Email(Notification):

    def generate_content(self) -> str:
        return f"EMAIL: {self.contenu}"


class Push(Notification):

    def generate_content(self) -> str:
        return f"PUSH: {self.contenu}"


class Slack(Notification):

    def generate_content(self) -> str:
        return f"SLACK: {self.contenu}"
