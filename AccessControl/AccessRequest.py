import uuid
import datetime


class AccessRequest:
    """Demande d'accès : une personne, un badge, une salle, un instant."""

    def __init__(self, requester, badge, room, requested_at=None):
        """Crée une demande datée, à défaut de l'instant courant."""
        self.request_id = str(uuid.uuid4())
        self.requested_at = requested_at or datetime.datetime.now()
        self.requester = requester
        self.badge = badge
        self.room = room

    def get_request_id(self):
        """Identifiant de la demande."""
        return self.request_id

    def get_requested_at(self):
        """Instant de la demande."""
        return self.requested_at

    def get_requester(self):
        """Personne demandeuse."""
        return self.requester

    def get_badge(self):
        """Badge présenté."""
        return self.badge

    def get_room(self):
        """Salle visée."""
        return self.room

    def get_badge_id(self):
        """Identifiant du badge présenté."""
        return self.badge.get_badge_id() if self.badge is not None else None

    def get_room_id(self):
        """Identifiant de la salle visée, par accesseur ou attribut."""
        if self.room is None:
            return None
        getter = getattr(self.room, "get_id", None)
        if callable(getter):
            return getter()
        return getattr(self.room, "id", None)
