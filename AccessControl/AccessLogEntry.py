import datetime


class AccessLogEntry:
    """Ligne du journal de sécurité tenu par le SecurityRegistry."""

    def __init__(self, request_id, badge_id, room_id, granted, reason, timestamp=None):
        """Crée une ligne datée, à défaut de l'instant courant."""
        self.request_id = request_id
        self.badge_id = badge_id
        self.room_id = room_id
        self.granted = granted
        self.reason = reason
        self.timestamp = timestamp or datetime.datetime.now()

    def get_request_id(self):
        """Identifiant de la demande."""
        return self.request_id

    def get_badge_id(self):
        """Identifiant du badge."""
        return self.badge_id

    def get_room_id(self):
        """Identifiant de la salle."""
        return self.room_id

    def is_granted(self):
        """Vrai si l'accès avait été accordé."""
        return self.granted

    def get_reason(self):
        """Motif enregistré."""
        return self.reason

    def get_timestamp(self):
        """Instant de la demande."""
        return self.timestamp

    def __str__(self):
        """Ligne telle qu'affichée dans le journal."""
        status = "ACCORDÉ" if self.granted else "REFUSÉ "
        return (f"[{self.timestamp:%Y-%m-%d %H:%M}] {status} "
                f"badge={self.badge_id} room={self.room_id} : {self.reason}")
