from AccessHandler import AccessHandler
from AccessDecision import AccessDecision
from SecurityRegistry import SecurityRegistry


class BlacklistHandler(AccessHandler):
    """Maillon 4 : refuse tout badge inscrit sur la liste noire."""

    def __init__(self, security_registry=None):
        """Crée le maillon sur le SecurityRegistry, le singleton par défaut."""
        super().__init__()
        self.security_registry = security_registry or SecurityRegistry.get_instance()

    def get_security_registry(self):
        """SecurityRegistry consulté."""
        return self.security_registry

    def check(self, request):
        """Refuse un badge sur liste noire, l'absence étant traitée en amont."""
        badge = request.get_badge()
        if badge is None:
            return AccessDecision.allow()

        badge_id = badge.get_badge_id()
        if self.security_registry.is_blacklisted(badge_id):
            return AccessDecision.deny(
                type(self).__name__,
                f"Badge {badge_id} sur liste noire : "
                f"{self.security_registry.get_blacklist_reason(badge_id)}")

        return AccessDecision.allow()
