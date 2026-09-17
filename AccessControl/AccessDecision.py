class AccessDecision:
    """Résultat de la chaîne : accordé, ou refusé par un maillon précis."""

    def __init__(self, granted, reason, refused_by=None):
        """Crée une décision : verdict, motif, auteur du refus."""
        self.granted = granted
        self.reason = reason
        self.refused_by = refused_by

    @staticmethod
    def allow():
        """Décision favorable."""
        return AccessDecision(True, "Accès accordé")

    @staticmethod
    def deny(handler, reason):
        """Refus attribué au maillon nommé."""
        return AccessDecision(False, reason, handler)

    def is_granted(self):
        """Vrai si l'accès est accordé."""
        return self.granted

    def get_reason(self):
        """Motif de la décision."""
        return self.reason

    def get_refused_by(self):
        """Nom du maillon ayant refusé."""
        return self.refused_by

    def __bool__(self):
        """Permet de tester la décision dans un if."""
        return self.granted

    def __str__(self):
        """Résumé lisible de la décision."""
        if self.granted:
            return f"ACCORDÉ ({self.reason})"
        return f"REFUSÉ par {self.refused_by} ({self.reason})"
