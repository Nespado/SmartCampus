from abc import ABC, abstractmethod
from typing import List

from sujets_observateurs import EventPublisher, EventObserver, Sujet, Observateur
from evenements import CampusEvent, Evenement, Incendie, AlerteConso, CoursAnnule
from strategies_envoi import DeliveryStrategy, StrategieEnvoi
from factory import NotificationFactory, TypeNotification
from notifications import Notification


class ModuleCampus(EventPublisher, ABC):
    """Classe abstraite de base pour les modules du campus (Publisher)."""

    def __init__(self):
        self._observers: List[EventObserver] = []
        self._observateurs = self._observers
        self._events: List[CampusEvent] = []
        self._evenements = self._events

    def add_observer(self, observer: EventObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def ajouter_observateur(self, observateur: EventObserver) -> None:
        self.add_observer(observateur)

    def remove_observer(self, observer: EventObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def retirer_observateur(self, observateur: EventObserver) -> None:
        self.remove_observer(observateur)

    def notify_observers(self, event: CampusEvent) -> None:
        for observer in list(self._observers):
            observer.update(event)

    def notifier_observateurs(self, evenement: CampusEvent) -> None:
        self.notify_observers(evenement)

    def emettre_evenement(self, evenement: CampusEvent) -> None:
        self._events.append(evenement)
        print(
            f"[{self.__class__.__name__}] "
            f"Événement émis : {evenement.description}"
        )
        self.notify_observers(evenement)

    def emit_event(self, event: CampusEvent) -> None:
        self.emettre_evenement(event)

    @abstractmethod
    def emettreEvenement(self):
        pass


class ModuleAcces(ModuleCampus):

    def detecter_incendie(
        self,
        date_ev,
        desc,
        localisation
    ):
        incendie = Incendie(
            date_ev,
            desc,
            localisation
        )
        self.emettre_evenement(incendie)

    def emettreEvenement(self):
        pass


class ModuleEcoGestion(ModuleCampus):

    def detecter_alerte_conso(
        self,
        date_ev,
        desc,
        niveau,
        consommation
    ):
        alerte = AlerteConso(
            date_ev,
            desc,
            niveau,
            consommation
        )
        self.emettre_evenement(alerte)

    def emettreEvenement(self):
        pass


class ModuleReservation(ModuleCampus):

    def annuler_cours(
        self,
        date_ev,
        desc,
        nom_cours,
        raison
    ):
        cours = CoursAnnule(
            date_ev,
            desc,
            nom_cours,
            raison
        )
        self.emettre_evenement(cours)

    def emettreEvenement(self):
        pass


class NotificationService(EventObserver):
    """Service d'écoute des événements campus et d'envoi des notifications (Groupe 1)."""

    def __init__(
        self,
        strategies: List[DeliveryStrategy] | None = None,
        recipient: str = "admin@campus.fr",
    ):
        self.strategies: List[DeliveryStrategy] = strategies if strategies is not None else []
        self.recipient = recipient
        self.destinataire = recipient

    def update(self, event: CampusEvent) -> None:
        self.handle_event(event)

    def mettre_a_jour(self, evenement: CampusEvent) -> None:
        self.update(evenement)

    def handle_event(self, event: CampusEvent) -> None:
        print(
            f"[NotificationService] "
            f"Traitement de l'événement : {event.description}"
        )
        notification = NotificationFactory.create(event, self.recipient)
        self.send(notification)

    def traiter_evenement(self, evenement: CampusEvent) -> None:
        self.handle_event(evenement)

    def send(self, notification: Notification) -> None:
        for strategy in self.strategies:
            strategy.send(notification)

    def envoyer(self, notification: Notification) -> None:
        self.send(notification)


# Alias français conservés pour compatibilité
ServiceNotification = NotificationService
EventPublisher = ModuleCampus

__all__ = [
    "ModuleCampus",
    "ModuleAcces",
    "ModuleEcoGestion",
    "ModuleReservation",
    "NotificationService",
    "ServiceNotification",
    "EventPublisher",
]
