from abc import ABC, abstractmethod


class Commande(ABC):
    """Interface commune aux commandes réversibles."""

    @abstractmethod
    def executer(self):
        pass

    @abstractmethod
    def defaire(self):
        pass
