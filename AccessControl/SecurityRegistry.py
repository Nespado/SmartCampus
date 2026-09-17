class SecurityRegistry:
    """Singleton : journal des accès et liste noire des badges."""

    __instance = None

    def __init__(self):
        """Crée le registre vide, une seule fois."""
        if SecurityRegistry.__instance is not None:
            raise RuntimeError("SecurityRegistry est un singleton : utiliser get_instance()")
        self.access_log = []
        self.blacklisted_badge_ids = set()
        self.blacklist_reasons = {}

    @staticmethod
    def get_instance():
        """Instance unique, créée au premier appel."""
        if SecurityRegistry.__instance is None:
            SecurityRegistry.__instance = SecurityRegistry()
        return SecurityRegistry.__instance

    def record(self, entry):
        """Ajoute une ligne au journal."""
        self.access_log.append(entry)

    def is_blacklisted(self, badge_id):
        """Vrai si le badge est sur liste noire."""
        return badge_id in self.blacklisted_badge_ids

    def blacklist_badge(self, badge_id, reason):
        """Inscrit un badge sur liste noire avec son motif."""
        self.blacklisted_badge_ids.add(badge_id)
        self.blacklist_reasons[badge_id] = reason

    def remove_from_blacklist(self, badge_id):
        """Retire un badge de la liste noire."""
        self.blacklisted_badge_ids.discard(badge_id)
        self.blacklist_reasons.pop(badge_id, None)

    def get_blacklist_reason(self, badge_id):
        """Motif de la mise en liste noire."""
        return self.blacklist_reasons.get(badge_id, "Badge sur liste noire")

    def get_history(self, badge_id):
        """Historique des accès d'un badge."""
        return [e for e in self.access_log if e.get_badge_id() == badge_id]

    def get_access_log(self):
        """Journal complet."""
        return list(self.access_log)

    def reset(self):
        """Vide le registre : réservé aux tests et à la démo."""
        self.access_log.clear()
        self.blacklisted_badge_ids.clear()
        self.blacklist_reasons.clear()
