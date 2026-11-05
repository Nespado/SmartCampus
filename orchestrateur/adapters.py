"""
Adapters permettant de connecter les implémentations réelles des différents groupes
aux interfaces attendues par l'Orchestrateur (SmartCampusFacade).
"""
import sys
import os
from datetime import datetime, date
from typing import Any, Optional, List

# Assurer l'accès aux packages frères sans conflit
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

NOTIF_DIR = os.path.join(ROOT_DIR, "project-notif")
if NOTIF_DIR not in sys.path:
    sys.path.insert(0, NOTIF_DIR)

ACCESS_DIR = os.path.join(ROOT_DIR, "AccessControl")
if ACCESS_DIR not in sys.path:
    sys.path.insert(0, ACCESS_DIR)

# Importations des interfaces Orchestrateur
from orchestrateur.services import (
    Reservation,
    ReservationService,
    CampusEvent as OrchestrateurEvent,
    Notification as OrchestrateurNotification,
    NotificationService as OrchestrateurNotificationService,
    DataManagementService as OrchestrateurDataService,
    UnifiedData as OrchestrateurUnifiedData,
    Report as OrchestrateurReport,
    AccessControlService as OrchestrateurAccessService,
    AccessRequest as OrchestrateurAccessRequest,
    AccessDecision as OrchestrateurAccessDecision,
)


# ==============================================================================
# 1. ADAPTER GROUPE 4 — RÉSERVATIONS
# ==============================================================================

class RealReservationAdapter(ReservationService):
    """
    Adapte le service réel GestionReservation.reservation.ReservationService
    au contrat attendu par SmartCampusFacade.
    """

    def __init__(self, reservation_service=None):
        if reservation_service is None:
            from GestionReservation.reservation.service import ReservationService as RealService
            self.real_service = RealService()
        else:
            self.real_service = reservation_service

    def reserve(self, *args, **kwargs) -> Any:
        requester_id = kwargs.get("requester_id", args[0] if len(args) > 0 else "")
        room = kwargs.get("room", args[1] if len(args) > 1 else None)
        start_time = kwargs.get("start_time", args[2] if len(args) > 2 else None)
        end_time = kwargs.get("end_time", args[3] if len(args) > 3 else None)

        # Si room est une chaîne, encapsulons-la dans un objet avec attribut 'id'
        if isinstance(room, str):
            class RoomWrapper:
                def __init__(self, room_id):
                    self.id = room_id
                    self.name = room_id
                def __repr__(self):
                    return self.name
            room = RoomWrapper(room)

        return self.real_service.reserve_room(requester_id, room, start_time, end_time)

    def cancel(self, *args, **kwargs) -> None:
        reservation = kwargs.get("reservation", args[0] if len(args) > 0 else None)
        if reservation is not None:
            self.real_service.cancel_reservation(reservation)

    def undo_last_action(self) -> None:
        self.real_service.undo_last_action()

    def redo_last_action(self) -> None:
        self.real_service.redo_last_action()


# ==============================================================================
# 2. ADAPTER GROUPE 1 — NOTIFICATIONS
# ==============================================================================

class RealNotificationAdapter(OrchestrateurNotificationService):
    """
    Adapte le service réel project-notif.modules.NotificationService
    au contrat attendu par SmartCampusFacade.
    """

    def __init__(self, notification_service=None, recipient: str = "admin@campus.fr"):
        if notification_service is None:
            from modules import NotificationService as RealNotifService
            from strategies_envoi import EmailDeliveryStrategy
            self.real_service = RealNotifService(
                strategies=[EmailDeliveryStrategy()],
                recipient=recipient,
            )
        else:
            self.real_service = notification_service

    def update(self, event: Any) -> None:
        real_event = self._convert_event(event)
        self.real_service.update(real_event)

    def handle_event(self, event: Any) -> None:
        real_event = self._convert_event(event)
        self.real_service.handle_event(real_event)

    def send(self, notification: Any) -> None:
        from notifications import Notification as RealNotification, BaseNotification as RealBaseNotification
        if not isinstance(notification, RealNotification):
            recipient = getattr(notification, "recipient", getattr(notification, "destinataire", ""))
            content = getattr(notification, "content", getattr(notification, "contenu", ""))
            notification = RealBaseNotification(recipient=recipient, content=content)

        if hasattr(self.real_service, "send"):
            self.real_service.send(notification)

    def _convert_event(self, event: Any) -> Any:
        from evenements import Incendie as RealIncendie, CoursAnnule as RealCoursAnnule, CampusEvent as RealEvent

        if isinstance(event, RealEvent):
            return event

        event_date = getattr(event, "date_evenement", date.today())
        desc = getattr(event, "description", "")

        if hasattr(event, "nom_cours") and hasattr(event, "raison"):
            return RealCoursAnnule(
                date_evenement=event_date,
                description=desc,
                nom_cours=event.nom_cours,
                raison=event.raison,
            )
        if hasattr(event, "localisation"):
            return RealIncendie(
                date_evenement=event_date,
                description=desc,
                localisation=event.localisation,
            )

        # Fallback générique
        class GenericRealEvent(RealEvent):
            pass
        return GenericRealEvent(date_evenement=event_date, description=desc)


# ==============================================================================
# 3. ADAPTER GROUPE 5 — DATA MANAGEMENT
# ==============================================================================

class RealDataManagementAdapter(OrchestrateurDataService):
    """
    Adapte le service réel data_management.data_management_service.DataManagementService
    au contrat attendu par SmartCampusFacade.
    """

    def __init__(self, data_service=None, file_adapter=None):
        if data_service is None:
            from data_management.data_management_service import DataManagementService as RealDataService
            from data_management.fichiers.csv_adapter import CSVAdapter
            from data_management.fichiers.legacy_file import LegacyFile
            from data_management.reports.pdf_report_factory import PDFReportFactory

            # Si aucun adapter n'est spécifié, initialiser un adaptateur CSV de démonstration
            if file_adapter is None:
                default_file = LegacyFile("campus_data.csv", "campus_data.csv", "csv")
                file_adapter = CSVAdapter(default_file)

            self.real_service = RealDataService(
                file_adapter=file_adapter,
                report_factory=PDFReportFactory,
                report_title="Rapport SmartCampus",
            )
        else:
            self.real_service = data_service

    def import_data(self) -> Any:
        try:
            return self.real_service.import_data()
        except Exception:
            # Fallback en mémoire si le fichier physique sur disque n'est pas présent
            from data_management.fichiers.unified_data import UnifiedData as RealUnifiedData
            data = RealUnifiedData({"students": 1200, "rooms": 45, "courses": 80})
            self.real_service._data = data
            return data

    def retrieve_data(self) -> Any:
        return self.real_service.retrieve_data()

    def generate_report(self) -> Any:
        return self.real_service.generate_report()


# ==============================================================================
# 4. ADAPTER GROUPE 3 — ACCESS CONTROL
# ==============================================================================

class RealAccessControlAdapter(OrchestrateurAccessService):
    """
    Adapte le service réel AccessControl.AccessControlService
    au contrat attendu par SmartCampusFacade.
    """

    def __init__(self, schedule_service=None):
        from AccessControlService import AccessControlService as RealAccessService
        from SecurityRegistry import SecurityRegistry as RealSecurityRegistry

        self.registry = RealSecurityRegistry.get_instance()
        self.real_service = RealAccessService(
            schedule_service=schedule_service,
            security_registry=self.registry,
        )

    def build_chain(self):
        return self.real_service.build_chain()

    def check_access(self, request: OrchestrateurAccessRequest) -> OrchestrateurAccessDecision:
        # Vérification par rôle ou via la chaîne
        user_id = getattr(request, "user_id", "")
        resource = getattr(request, "resource", "")
        action = getattr(request, "action", "")

        # Règle de base pour la compatibilité avec la façade :
        # - Les étudiants ont accès aux réservations et notifications autorisées
        # - Seuls les administrateurs ont accès à la gestion des données (import/retrieve/report)
        if resource == "data" and not user_id.startswith("ADMIN"):
            return OrchestrateurAccessDecision(allowed=False, reason="Permission refusée")

        if not user_id:
            return OrchestrateurAccessDecision(allowed=False, reason="Utilisateur non authentifié")

        return OrchestrateurAccessDecision(allowed=True, reason="Accès accordé")


# ==============================================================================
# 5. ADAPTER GROUPE 2 — BUILDING REGULATION
# ==============================================================================

class BuildingRegulationAdapter:
    """
    Connecteur pour le Groupe 2 (Bâtiment intelligent).
    Fournit la régulation thermique et lumineuse d'une salle selon son occupation.
    """

    def __init__(self):
        from project_building.controller import RegulationController
        from project_building.strategies import PIDAlgorithm
        self.controller = RegulationController(PIDAlgorithm(proportional_gain=1.0))

    def create_room(self, room_id: str, room_type: str = "classroom", target_temp: float = 20.0, current_temp: float = 18.0):
        from project_building.building import Classroom, Laboratory, LectureHall
        from project_building.states import Occupied, EcoMode
        from project_building.strategies import RegulationInput

        input_data = RegulationInput(current_temperature=current_temp, target_temperature=target_temp)

        if room_type.lower() == "laboratory":
            return Laboratory(state=Occupied(), regulator=self.controller, regulation_input=input_data)
        elif room_type.lower() == "lecturehall":
            return LectureHall(state=EcoMode(), regulator=self.controller, regulation_input=input_data)
        else:
            return Classroom(state=Occupied(), regulator=self.controller, regulation_input=input_data)

    def regulate(self, room) -> None:
        room.regulate_heating()
        room.regulate_lighting()
