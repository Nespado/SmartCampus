from Person import Person


class Student(Person):
    """Étudiant, habilitation la plus basse."""

    ROLE = "STUDENT"

    def __init__(self, name):
        """Crée un étudiant de rôle STUDENT."""
        super().__init__(name, Student.ROLE)
