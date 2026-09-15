
from abc import ABC, abstractmethod
from typing import List

from sujets_observateurs import Sujet, Observateur
from evenements import Evenement, Incendie, AlerteConso, CoursAnnule
from strategies_envoi import StrategieEnvoi
from factory import NotificationFactory, TypeNotification

class ModuleCampus(Sujet, ABC):

    def __init__(self):
        self._observateurs: List[Observateur] = []
        self._evenements: List[Evenement] = []

    def add_observer(self, observateur: Observateur):
        if observateur not in self._observateurs:
            self._observateurs.append(observateur)

    def ajouter_observateur(self, observateur: Observateur):
        self.add_observer(observateur)

    def remove_observer(self, observateur: Observateur):
        if observateur in self._observateurs:
            self._observateurs.remove(observateur)

    def retirer_observateur(self, observateur: Observateur):
        self.remove_observer(observateur)

    def notify_observers(self, evenement: Evenement):
        for observateur in self._observateurs:
            observateur.update(evenement)

    def notifier_observateurs(self, evenement: Evenement):
        self.notify_observers(evenement)

    def emettre_evenement(self, evenement: Evenement):
        self._evenements.append(evenement)

        print(
            f"[{self.__class__.__name__}] "
            f"Événement émis : {evenement.description}"
        )

        self.notify_observers(evenement)

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


class ServiceNotification(Observateur):

    def __init__(self, strategies: List[StrategieEnvoi]):
        self.strategies = strategies

    def update(self, evenement: Evenement):
        self.handle_event(evenement)

    def mettre_a_jour(self, evenement: Evenement):
        self.update(evenement)

    def traiter_evenement(self, evenement: Evenement):
        self.handle_event(evenement)

    def handle_event(self, evenement: Evenement):

        print(
            f"[ServiceNotification] "
            f"Traitement de l'événement : {evenement.description}"
        )

        notification = NotificationFactory.create(evenement, "admin@campus.fr")

        self.send(notification)

    def send(self, notification):
        for strategie in self.strategies:
            strategie.envoyer(notification)


# Noms anglais du contrat Groupe 1, sans supprimer l'API française existante.
EventPublisher = ModuleCampus
NotificationService = ServiceNotification
