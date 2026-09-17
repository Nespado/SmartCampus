import datetime


class AccessEvent:
    """Événement publié par l'AccessControlService lors d'un refus.

    Remplaçant local du CampusEvent du Groupe 1 : dès que leur paquet existe,
    en faire `class AccessEvent(CampusEvent)` en gardant les champs.
    """

    def __init__(self, request_id, badge_id, room_id, reason, refused_by, date=None):
        """Crée l'événement et compose sa description."""
        self.date = date or datetime.datetime.now()
        self.description = f"Accès refusé sur la salle {room_id} : {reason}"
        self.request_id = request_id
        self.badge_id = badge_id
        self.room_id = room_id
        self.reason = reason
        self.refused_by = refused_by

    def get_date(self):
        """Date du refus."""
        return self.date

    def get_description(self):
        """Message destiné aux observateurs."""
        return self.description

    def __str__(self):
        """Description de l'événement."""
        return self.description
