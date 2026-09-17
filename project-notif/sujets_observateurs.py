from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from evenements import CampusEvent


class EventObserver(ABC):
    """Interface pour les observateurs d'événements (Groupe 1)."""

    @abstractmethod
    def update(self, event: 'CampusEvent') -> None:
        pass

    def mettre_a_jour(self, e: 'CampusEvent') -> None:
        """Alias français pour compatibilité."""
        self.update(e)


# Alias français pour compatibilité
Observateur = EventObserver


class EventPublisher(ABC):
    """Interface / classe abstraite pour le pattern Observer (Groupe 1)."""

    @abstractmethod
    def add_observer(self, observer: EventObserver) -> None:
        pass

    def ajouter_observateur(self, observateur: EventObserver) -> None:
        """Alias français pour compatibilité."""
        self.add_observer(observateur)

    @abstractmethod
    def remove_observer(self, observer: EventObserver) -> None:
        pass

    def retirer_observateur(self, observateur: EventObserver) -> None:
        """Alias français pour compatibilité."""
        self.remove_observer(observateur)

    @abstractmethod
    def notify_observers(self, event: 'CampusEvent') -> None:
        pass

    def notifier_observateurs(self, evenement: 'CampusEvent') -> None:
        """Alias français pour compatibilité."""
        self.notify_observers(evenement)


# Alias français pour compatibilité
Sujet = EventPublisher


class Admin:
    """Import Groupe 6 - Représente un administrateur"""

    def gerer_sujet(self, sujet: EventPublisher):
        pass