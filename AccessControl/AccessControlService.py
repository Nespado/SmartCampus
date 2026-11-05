from AccessEvent import AccessEvent
from AccessLogEntry import AccessLogEntry
from SecurityRegistry import SecurityRegistry
from BadgeValidityHandler import BadgeValidityHandler
from ScheduleCheckHandler import ScheduleCheckHandler
from RolePermissionHandler import RolePermissionHandler
from BlacklistHandler import BlacklistHandler


class AccessControlService:
    """Point d'entrée du Groupe 3.

    Construit la chaîne de responsabilité, y fait passer une AccessRequest,
    tient le SecurityRegistry à jour et joue le rôle de Sujet (EventPublisher)
    du Groupe 1 en notifiant ses observateurs à chaque refus.
    """

    def __init__(self, schedule_service=None, security_registry=None, role_clearance=None):
        """Crée le service sur ses collaborateurs et assemble la chaîne."""
        self.security_registry = security_registry or SecurityRegistry.get_instance()
        self.schedule_service = schedule_service
        self.role_clearance = role_clearance
        self.observers = []
        self.chain = self.build_chain()

    def build_chain(self):
        """Assemble les quatre maillons et retourne la tête de chaîne."""
        badge_validity = BadgeValidityHandler()
        schedule_check = ScheduleCheckHandler(self.schedule_service)
        role_permission = RolePermissionHandler(self.role_clearance)
        blacklist = BlacklistHandler(self.security_registry)

        badge_validity.set_next(schedule_check).set_next(role_permission).set_next(blacklist)
        return badge_validity

    def check_access(self, request):
        """Exécute la chaîne, journalise la demande et signale tout refus."""
        decision = self.chain.handle(request)

        self.security_registry.record(AccessLogEntry(
            request_id=request.get_request_id(),
            badge_id=request.get_badge_id(),
            room_id=request.get_room_id(),
            granted=decision.is_granted(),
            reason=decision.get_reason(),
            timestamp=request.get_requested_at(),
        ))

        if not decision.is_granted():
            self.notify_observers(AccessEvent(
                request_id=request.get_request_id(),
                badge_id=request.get_badge_id(),
                room_id=request.get_room_id(),
                reason=decision.get_reason(),
                refused_by=decision.get_refused_by(),
                date=request.get_requested_at(),
            ))

        return decision

    def get_chain(self):
        """Tête de la chaîne de responsabilité."""
        return self.chain

    def get_security_registry(self):
        """SecurityRegistry alimenté par le service."""
        return self.security_registry

    def add_observer(self, observer):
        """Abonne un observateur, sans doublon."""
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        """Désabonne un observateur."""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, event):
        """Diffuse un événement à tous les observateurs abonnés."""
        for observer in list(self.observers):
            observer.update(event)
