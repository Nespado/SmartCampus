from abc import ABC, abstractmethod
from typing import List
from evenements import Evenement

class Sujet(ABC):
    """Interface pour le pattern Observer"""
    @abstractmethod
    def add_observer(self, observer: 'Observateur'):
        pass

    def ajouter_observateur(self, observateur: 'Observateur'):
        self.add_observer(observateur)

    @abstractmethod
    def remove_observer(self, observer: 'Observateur'):
        pass

    def retirer_observateur(self, observateur: 'Observateur'):
        self.remove_observer(observateur)

    @abstractmethod
    def notify_observers(self, event: Evenement):
        pass

    def notifier_observateurs(self, evenement: Evenement):
        self.notify_observers(evenement)


class Observateur(ABC):
    """Interface pour les observateurs"""
    @abstractmethod
    def update(self, event: Evenement):
        pass

    def mettre_a_jour(self, e: Evenement):
        self.update(e)


EventObserver = Observateur


class Admin:
    """Import Groupe 6 - Représente un administrateur"""
    def gerer_sujet(self, sujet: Sujet):
        pass    