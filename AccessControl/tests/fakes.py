"""Doublures minimales des classes appartenant aux autres groupes.

Room (domaine partagé) et ScheduleService (Groupe 4) ne sont pas à nous : le
Groupe 3 ne dépend que de Room.is_open_at() / clearance_level et de
ScheduleService.has_reservation(). Ces doublures respectent ce seul contrat.
"""


class FakeRoom:
    """Tient lieu de Room, ouverte sur une plage horaire fixe."""

    def __init__(self, room_id, clearance_level=1, open_from=8, open_to=18):
        """Crée une salle avec son niveau et ses heures d'ouverture."""
        self.id = room_id
        self.clearance_level = clearance_level
        self.open_from = open_from
        self.open_to = open_to

    def get_id(self):
        """Identifiant de la salle."""
        return self.id

    def is_open_at(self, at):
        """Vrai si l'instant tombe dans les heures d'ouverture."""
        return self.open_from <= at.hour < self.open_to


class FakeScheduleService:
    """Tient lieu de ScheduleService, sur une liste en mémoire."""

    def __init__(self):
        """Crée un planning sans réservation."""
        self.reservations = []

    def add(self, requester_id, room, start, end):
        """Enregistre la réservation d'une salle sur une plage."""
        self.reservations.append((requester_id, room, start, end))

    def has_reservation(self, requester_id, room, at):
        """Vrai si le demandeur a réservé cette salle à cet instant."""
        return any(r_id == requester_id and r_room is room and start <= at <= end
                   for r_id, r_room, start, end in self.reservations)


class RecordingObserver:
    """Tient lieu d'EventObserver du Groupe 1, en gardant ce qu'il reçoit."""

    def __init__(self):
        """Crée un observateur n'ayant rien reçu."""
        self.events = []

    def update(self, event):
        """Mémorise l'événement publié par le service."""
        self.events.append(event)
