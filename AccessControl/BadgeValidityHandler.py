from AccessHandler import AccessHandler
from AccessDecision import AccessDecision


class BadgeValidityHandler(AccessHandler):
    """Maillon 1 : badge présent, actif, non expiré et appartenant au demandeur."""

    def check(self, request):
        """Refuse un badge absent, désactivé, expiré ou emprunté."""
        handler = type(self).__name__
        badge = request.get_badge()
        if badge is None:
            return AccessDecision.deny(handler, "Aucun badge présenté")

        if not badge.is_active():
            return AccessDecision.deny(
                handler, f"Badge {badge.get_badge_id()} désactivé")

        if badge.is_expired(request.get_requested_at()):
            return AccessDecision.deny(
                handler, f"Badge {badge.get_badge_id()} expiré le {badge.get_expires_on()}")

        requester = request.get_requester()
        if requester is not None and badge.get_owner_id() != requester.get_id():
            return AccessDecision.deny(
                handler, f"Badge {badge.get_badge_id()} n'appartient pas à {requester.get_name()}")

        return AccessDecision.allow()
