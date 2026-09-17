class Equipment:
    """Représente un matériel du campus."""

    def __init__(self, equipment_id, name, available=True):
        self.id = equipment_id
        self.name = name
        self.available = available
