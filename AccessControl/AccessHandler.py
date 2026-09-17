from abc import ABC, abstractmethod


class AccessHandler(ABC):
    """Chaîne de responsabilité : un maillon = une règle d'accès."""

    def __init__(self):
        """Crée un maillon sans successeur."""
        self.next = None

    def set_next(self, next_handler):
        """Branche le successeur et le retourne, pour chaîner les maillons."""
        self.next = next_handler
        return next_handler

    def get_next(self):
        """Successeur du maillon."""
        return self.next

    def handle(self, request):
        """Applique la règle, s'arrête au premier refus, sinon délègue."""
        decision = self.check(request)
        if not decision.is_granted():
            return decision
        if self.next is not None:
            return self.next.handle(request)
        return decision

    @abstractmethod
    def check(self, request):
        """Applique la seule règle du maillon."""
        raise NotImplementedError
