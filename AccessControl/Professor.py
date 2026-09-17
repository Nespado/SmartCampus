from Person import Person


class Professor(Person):
    """Enseignant, habilitation élevée."""

    ROLE = "PROFESSOR"

    def __init__(self, name):
        """Crée un professeur de rôle PROFESSOR."""
        super().__init__(name, Professor.ROLE)
