import uuid


class Person:
    """Classe abstraite d'une personne du campus."""

    def __init__(self, name, role):
        """Crée une personne avec un id généré."""
        if type(self) is Person:
            raise TypeError("Person est abstraite : instancier Student ou Professor")
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role

    def get_id(self):
        """Identifiant de la personne."""
        return self.id

    def get_name(self):
        """Nom de la personne."""
        return self.name

    def get_role(self):
        """Rôle de la personne."""
        return self.role

    def __repr__(self):
        """Représentation lisible."""
        return f"{type(self).__name__}(name={self.name!r}, role={self.role!r})"
