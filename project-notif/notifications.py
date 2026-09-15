from abc import ABC, abstractmethod


class Notification(ABC):
    """Classe abstraite représentant une notification."""

    def __init__(self, destinataire: str, contenu: str):
        self.destinataire = destinataire
        self.contenu = contenu

    @abstractmethod
    def generate_content(self) -> str:
        pass

    def generer_contenu(self) -> str:
        """Alias français conservé pour la compatibilité avec l'ancien code."""
        return self.generate_content()


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
