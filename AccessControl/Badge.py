import datetime


class Badge:
    """Badge physique appartenant à une personne."""

    def __init__(self, badge_id, owner_id, expires_on, active=True):
        """Crée un badge lié à son propriétaire."""
        self.badge_id = badge_id
        self.owner_id = owner_id
        self.expires_on = expires_on
        self.active = active

    def is_expired(self, at):
        """Vrai si le badge est expiré à cet instant."""
        if self.expires_on is None:
            return False
        if isinstance(self.expires_on, datetime.datetime):
            return at > self.expires_on
        moment = at.date() if isinstance(at, datetime.datetime) else at
        return moment > self.expires_on

    def is_active(self):
        """Vrai si le badge est actif."""
        return self.active

    def deactivate(self):
        """Désactive le badge."""
        self.active = False

    def get_badge_id(self):
        """Identifiant du badge."""
        return self.badge_id

    def get_owner_id(self):
        """Identifiant du propriétaire."""
        return self.owner_id

    def get_expires_on(self):
        """Date d'expiration."""
        return self.expires_on

    def __repr__(self):
        """Représentation lisible."""
        return f"Badge(badge_id={self.badge_id!r}, owner_id={self.owner_id!r})"
