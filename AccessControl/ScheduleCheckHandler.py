from AccessHandler import AccessHandler
from AccessDecision import AccessDecision


class ScheduleCheckHandler(AccessHandler):
    """Maillon 2 : salle ouverte à cet instant, ou couverte par une réservation.

    Dépend du ScheduleService du Groupe 4 (has_reservation) et de
    Room.is_open_at() du domaine partagé.
    """

    def __init__(self, schedule_service=None):
        """Crée le maillon sur le ScheduleService des réservations."""
        super().__init__()
        self.schedule_service = schedule_service

    def get_schedule_service(self):
        """ScheduleService consulté."""
        return self.schedule_service

    def check(self, request):
        """Accorde une salle ouverte, sinon exige une réservation couvrant l'instant."""
        handler = type(self).__name__
        room = request.get_room()
        if room is None:
            return AccessDecision.deny(handler, "Aucune salle visée par la demande")

        at = request.get_requested_at()
        if room.is_open_at(at):
            return AccessDecision.allow()

        requester = request.get_requester()
        requester_id = requester.get_id() if requester is not None else None
        if (self.schedule_service is not None
                and self.schedule_service.has_reservation(requester_id, room, at)):
            return AccessDecision.allow()

        return AccessDecision.deny(
            handler, f"Salle {request.get_room_id()} fermée à {at:%H:%M}, "
                     f"aucune réservation ne la couvre")
