"""
Interfaces et Stubs des services externes (Groupe 4, Groupe 1 et Groupe 5).
Conforme au document de référence Python POO SmartCampus :
- Convention : classes en PascalCase, méthodes/arguments en snake_case.
Permet à l'Orchestrateur (Groupe 6) de fonctionner de manière autonome sans importer les répertoires externes.
"""
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any, List, Optional


# ==============================================================================
# 1. CONTRATS GROUPE 4 — RÉSERVATIONS
# ==============================================================================

class Reservation(ABC):
    """Interface Reservation (Groupe 4)."""

    @abstractmethod
    def reserve(self) -> None:
        """Exécute / active la réservation."""
        pass

    @abstractmethod
    def cancel(self) -> None:
        """Annule la réservation."""
        pass


class ReservationStub(Reservation):
    """Implémentation concrète stub d'une réservation pour tests et démonstrations."""

    def __init__(self, details: str = "Réservation"):
        self.details = details
        self.active = False

    def reserve(self) -> None:
        self.active = True

    def cancel(self) -> None:
        self.active = False

    def __repr__(self) -> str:
        return f"ReservationStub({self.details}, active={self.active})"


class ReservationService(ABC):
    """
    Interface du service de réservation (Groupe 4).
    Méthodes conformes au référentiel :
    - reserve() -> Reservation
    - cancel() -> None
    - undo_last_action() -> None
    - redo_last_action() -> None
    """

    @abstractmethod
    def reserve(self, *args, **kwargs) -> Reservation:
        pass

    @abstractmethod
    def cancel(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def undo_last_action(self) -> None:
        pass

    @abstractmethod
    def redo_last_action(self) -> None:
        pass


class ReservationServiceStub(ReservationService):
    """Stub simulant le ReservationService du Groupe 4."""

    def __init__(self):
        self.history: List[Reservation] = []

    def reserve(self, *args, **kwargs) -> Reservation:
        requester_id = kwargs.get("requester_id", args[0] if len(args) > 0 else "inconnu")
        room = kwargs.get("room", args[1] if len(args) > 1 else "salle")
        start_time = kwargs.get("start_time", args[2] if len(args) > 2 else "")
        end_time = kwargs.get("end_time", args[3] if len(args) > 3 else "")

        res = ReservationStub(f"room={room}, requester={requester_id}, from={start_time}, to={end_time}")
        res.reserve()
        self.history.append(res)
        return res

    def cancel(self, *args, **kwargs) -> None:
        if args and isinstance(args[0], Reservation):
            args[0].cancel()
        print("[ReservationService (Groupe 4)] Annulation de la réservation effectuée.")

    def undo_last_action(self) -> None:
        print("[ReservationService (Groupe 4)] Annulation de la dernière action (Undo).")

    def redo_last_action(self) -> None:
        print("[ReservationService (Groupe 4)] Rétablissement de la dernière action (Redo).")


# ==============================================================================
# 2. CONTRATS GROUPE 1 — NOTIFICATIONS
# ==============================================================================

class CampusEvent(ABC):
    """Classe abstraite de base représentant un événement campus (Groupe 1)."""

    def __init__(self, date_evenement: Optional[date] = None, description: str = ""):
        self.date_evenement = date_evenement or date.today()
        self.description = description

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(description='{self.description}')"


class Incendie(CampusEvent):
    """Événement d'incendie (Groupe 1)."""

    def __init__(self, localisation: str, description: str = "Alerte incendie", date_evenement: Optional[date] = None):
        super().__init__(date_evenement=date_evenement, description=description)
        self.localisation = localisation


class CoursAnnule(CampusEvent):
    """Événement d'annulation de cours / réservation (Groupe 1)."""

    def __init__(self, nom_cours: str, raison: str, description: str = "", date_evenement: Optional[date] = None):
        desc = description or f"Cours '{nom_cours}' annulé : {raison}"
        super().__init__(date_evenement=date_evenement, description=desc)
        self.nom_cours = nom_cours
        self.raison = raison


class Notification(ABC):
    """Classe abstraite représentant une notification (Groupe 1)."""

    def __init__(self, recipient: str = "", content: str = ""):
        self.recipient = recipient
        self.content = content

    @abstractmethod
    def generate_content(self) -> str:
        """Génère le contenu textuel de la notification."""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(recipient='{self.recipient}', content='{self.generate_content()}')"


class BaseNotification(Notification):
    """Notification de base sans décorateur (Groupe 1)."""

    def generate_content(self) -> str:
        return self.content


class NotificationService(ABC):
    """
    Interface du service de notifications (Groupe 1).
    Méthodes conformes au référentiel :
    - update(event: CampusEvent) -> None
    - handle_event(event: CampusEvent) -> None
    - send(notification: Notification) -> None
    """

    @abstractmethod
    def update(self, event: CampusEvent) -> None:
        """Met à jour les observateurs suite à la publication d'un événement."""
        pass

    @abstractmethod
    def handle_event(self, event: CampusEvent) -> None:
        """Traite un événement campus pour déclencher des alertes."""
        pass

    @abstractmethod
    def send(self, notification: Notification) -> None:
        """Envoie la notification aux canaux configurés."""
        pass


class NotificationServiceStub(NotificationService):
    """Stub simulant le NotificationService du Groupe 1 pour tester la Façade."""

    def __init__(self, recipient: str = "admin@campus.fr"):
        self.recipient = recipient
        self.sent_notifications: List[Notification] = []
        self.received_events: List[CampusEvent] = []

    def update(self, event: CampusEvent) -> None:
        print(f"[NotificationService (Groupe 1)] update() reçu : {event}")
        self.handle_event(event)

    def handle_event(self, event: CampusEvent) -> None:
        print(f"[NotificationService (Groupe 1)] handle_event() traitement de : {event}")
        self.received_events.append(event)
        # Création et envoi automatique d'une notification pour l'événement
        notif = BaseNotification(recipient=self.recipient, content=f"Alerte : {event.description}")
        self.send(notif)

    def send(self, notification: Notification) -> None:
        self.sent_notifications.append(notification)
        print(f"[NotificationService (Groupe 1)] send() -> Destinataire : {notification.recipient} | Contenu : {notification.generate_content()}")


# ==============================================================================
# 3. CONTRATS GROUPE 5 — DATA MANAGEMENT
# ==============================================================================

class UnifiedData:
    """Représente les données unifiées importées du système."""

    def __init__(self, data: Any = None):
        self.data = data if data is not None else []

    def __repr__(self) -> str:
        return f"UnifiedData({self.data})"


class LegacyFile:
    """Représente un fichier provenant d'un ancien système."""

    def __init__(self, filename: str, content: Any = None):
        self.filename = filename
        self.content = content

    def __repr__(self) -> str:
        return f"LegacyFile({self.filename})"


class Report:
    """Représente un rapport généré à partir des données."""

    def __init__(self, title: str, content: Any = None):
        self.title = title
        self.content = content

    def __repr__(self) -> str:
        return f"Report(title={self.title})"


class DataManagementService(ABC):
    """
    Interface du service de gestion des données (Groupe 5).

    Méthodes conformes au modèle UML :
    - import_data() -> UnifiedData
    - retrieve_data() -> UnifiedData
    - generate_report() -> Report
    """

    @abstractmethod
    def import_data(self) -> UnifiedData:
        pass

    @abstractmethod
    def retrieve_data(self) -> UnifiedData:
        pass

    @abstractmethod
    def generate_report(self) -> Report:
        pass


class DataManagementServiceStub(DataManagementService):
    """Stub simulant le DataManagementService."""

    def __init__(self):
        self.files = []
        self.reports = []
        self.unified_data = UnifiedData()

    def import_data(self) -> UnifiedData:
        """
        Simule l'importation de fichiers Legacy
        et leur transformation en données unifiées.
        """
        print("[DataManagementService] Importation des données...")

        self.files = [
            LegacyFile("students.csv"),
            LegacyFile("rooms.csv"),
            LegacyFile("courses.csv"),
        ]

        self.unified_data = UnifiedData({
            "students": 1200,
            "rooms": 45,
            "courses": 80,
        })

        print(
            f"[DataManagementService] "
            f"{len(self.files)} fichiers importés."
        )

        return self.unified_data

    def retrieve_data(self) -> UnifiedData:
        """Simule la récupération des données unifiées."""
        print("[DataManagementService] Récupération des données...")
        return self.unified_data

    def generate_report(self) -> Report:
        """Simule la génération d'un rapport."""
        print("[DataManagementService] Génération du rapport...")

        report = Report(
            title="Rapport SmartCampus",
            content={
                "students": self.unified_data.data.get("students", 0),
                "rooms": self.unified_data.data.get("rooms", 0),
                "courses": self.unified_data.data.get("courses", 0),
            },
        )

        self.reports.append(report)
        return report
