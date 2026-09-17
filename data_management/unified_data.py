from dataclasses import dataclass


@dataclass
class UnifiedData:
    """Conteneur minimal partagé avec les futurs adapters de fichiers."""

    donnees: object
