from AccessHandler import AccessHandler
from AccessDecision import AccessDecision

DEFAULT_ROLE_CLEARANCE = {
    "STUDENT": 1,
    "STAFF": 2,
    "PROFESSOR": 3,
    "ADMIN": 4,
}


def _clearance_of(room):
    """Niveau d'habilitation de la salle, par accesseur ou attribut."""
    if room is None:
        return 0
    getter = getattr(room, "get_clearance_level", None)
    if callable(getter):
        return getter()
    return getattr(room, "clearance_level", 0)


class RolePermissionHandler(AccessHandler):
    """Maillon 3 : le rôle du demandeur doit atteindre le niveau de la salle."""

    def __init__(self, role_clearance=None):
        """Crée le maillon sur une table rôle vers niveau."""
        super().__init__()
        self.role_clearance = dict(role_clearance) if role_clearance else dict(DEFAULT_ROLE_CLEARANCE)

    def check(self, request):
        """Compare l'habilitation du rôle au niveau requis par la salle."""
        handler = type(self).__name__
        requester = request.get_requester()
        if requester is None:
            return AccessDecision.deny(handler, "Demandeur inconnu")

        role = requester.get_role()
        if role not in self.role_clearance:
            return AccessDecision.deny(handler, f"Rôle '{role}' inconnu")

        granted_level = self.role_clearance[role]
        required_level = _clearance_of(request.get_room())
        if granted_level < required_level:
            return AccessDecision.deny(
                handler, f"Rôle '{role}' (niveau {granted_level}) inférieur au niveau "
                         f"{required_level} requis par la salle {request.get_room_id()}")

        return AccessDecision.allow()
